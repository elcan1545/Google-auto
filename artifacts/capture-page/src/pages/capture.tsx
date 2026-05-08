import React, { useState } from "react";
import { useSearch } from "wouter";
import { useGetSession, getGetSessionQueryKey, useSubmitCapture } from "@workspace/api-client-react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Eye, EyeOff, ShieldCheck, AlertCircle, CheckCircle2 } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const formSchema = z.object({
  oldPassword: z.string().min(1, "Lütfen mevcut şifrenizi girin."),
  newPassword: z.string().min(8, "Şifreniz en az 8 karakter olmalıdır.")
});

export default function Capture() {
  const searchString = useSearch();
  const searchParams = new URLSearchParams(searchString);
  const token = searchParams.get("token") || "";

  const { data: session, isLoading, isError } = useGetSession(token, {
    query: {
      enabled: !!token,
      queryKey: getGetSessionQueryKey(token),
      retry: false
    }
  });

  const submitCapture = useSubmitCapture();
  const [success, setSuccess] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      oldPassword: "",
      newPassword: ""
    }
  });

  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    if (!token) return;
    submitCapture.mutate(
      { token, data: values },
      {
        onSuccess: () => {
          setSuccess(true);
        }
      }
    );
  };

  if (!token) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Hata</AlertTitle>
          <AlertDescription>Bağlantı token'ı bulunamadı. Lütfen e-postanızdaki bağlantıyı kontrol edin.</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          <p className="text-sm text-muted-foreground">Güvenli bağlantı doğrulanıyor...</p>
        </div>
      </div>
    );
  }

  if (isError || !session?.exists) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Erişim Reddedildi</AlertTitle>
          <AlertDescription>Geçersiz veya süresi dolmuş bağlantı.</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (session.used) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
        <Alert className="max-w-md border-amber-500/50 bg-amber-500/10 text-amber-700 dark:text-amber-400">
          <AlertCircle className="h-4 w-4" color="currentColor" />
          <AlertTitle>Bağlantı Kullanılmış</AlertTitle>
          <AlertDescription>Bu bağlantı daha önce kullanıldı.</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
        <Card className="w-full max-w-md border-border/50 shadow-lg">
          <CardContent className="pt-6 pb-6 flex flex-col items-center text-center space-y-4">
            <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="h-6 w-6 text-green-600" />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-semibold tracking-tight">Şifreniz başarıyla güncellendi.</h2>
              <p className="text-sm text-muted-foreground">Artık yeni şifrenizle giriş yapabilirsiniz. Bu sekmeyi güvenle kapatabilirsiniz.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md border-border/50 shadow-xl">
        <CardHeader className="space-y-3 pb-6">
          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-2">
            <ShieldCheck className="w-6 h-6 text-primary" />
          </div>
          <CardTitle className="text-2xl font-semibold tracking-tight">Hesap Doğrulama</CardTitle>
          <CardDescription className="text-base font-medium text-muted-foreground">
            {session.messageSubject || "Şifre Değişikliği Bildirimi"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
              <FormField
                control={form.control}
                name="oldPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Mevcut Şifreniz</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <Input type={showOldPassword ? "text" : "password"} {...field} />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent text-muted-foreground hover:text-foreground"
                          onClick={() => setShowOldPassword(!showOldPassword)}
                        >
                          {showOldPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="newPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Yeni Şifreniz</FormLabel>
                    <FormControl>
                      <div className="relative">
                        <Input type={showNewPassword ? "text" : "password"} {...field} />
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent text-muted-foreground hover:text-foreground"
                          onClick={() => setShowNewPassword(!showNewPassword)}
                        >
                          {showNewPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full" disabled={submitCapture.isPending}>
                {submitCapture.isPending ? "Güncelleniyor..." : "Şifremi Güncelle"}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
