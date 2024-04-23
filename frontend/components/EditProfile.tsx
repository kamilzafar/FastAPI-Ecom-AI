"use client"
import { updateUser } from "@/actions/editProfile"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useState } from "react"
import { useToast } from "./ui/use-toast"

type User = {
  name: string;
  email: string;
};

export function DialogDemo({name, email}: User) {
  let [username, setUsername] = useState(name) 
  const {toast} = useToast()
  const submit = async () => {
    await updateUser(username)
    toast({
      title: "Profile updated",
      description: "Your profile has been updated successfully",
    })
  }
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost">Edit Profile</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you&apos;re done.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={submit}>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">
              Username
            </Label>
            <Input
              id="name"
              defaultValue={username}
              className="col-span-3"
              onChange={(e) => setUsername(e.target.value)}
              about="username"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="text-right">
              Email
            </Label>
            <Input
              id="email"
              defaultValue={email}
              className="col-span-3"
              about="email"
              disabled
            />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit">Save changes</Button>
        </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
