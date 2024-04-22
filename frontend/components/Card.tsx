"use client"
import {
CreditCard,
LogOut,
} from "lucide-react"
import { Dialog } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import {
DropdownMenu,
DropdownMenuContent,
DropdownMenuGroup,
DropdownMenuItem,
DropdownMenuLabel,
DropdownMenuSeparator,
DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { useRouter } from "next/navigation"
import { myDeleteCookie } from "@/lib/auth"
import Link from "next/link"

export function DropdownMenuDemo({name}: {name: string}) {
    const router = useRouter()
    return (
    <Dialog>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost">{name}</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-36 bg-inherit">
          <DropdownMenuLabel>My Account</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <Link href="/orders" >
            <DropdownMenuItem onClick={()=>router.push("/orders")}>
              <CreditCard className="mr-2 h-4 w-4" />
              <span>View Orders</span>
            </DropdownMenuItem>
            </Link>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={() => {myDeleteCookie(); router.refresh()}}>
            <LogOut className="mr-2 h-4 w-4" />
            <span>Log out</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </Dialog>
    )
  }
  