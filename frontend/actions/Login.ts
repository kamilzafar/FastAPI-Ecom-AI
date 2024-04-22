"use server"
import { mySetCookie } from "@/lib/auth";

export const loginUser = async (username: string, password:string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
  try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/login`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData
      })

      const data = await res.json()
      if (data && data.access_token && data.refresh_token) {
        mySetCookie(data.access_token, data.refresh_token);
      }
      return data
  }
  catch (error) {
      console.log(error, "error");
      console.log("error is error");
  }
}