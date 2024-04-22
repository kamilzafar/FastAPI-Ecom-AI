"use client"
import { deleteCart } from "@/actions/delete_cart"
import { useRouter } from "next/navigation"
import { useToast } from "./ui/use-toast"
import { ToastAction } from "./ui/toast"

interface IDelete_products {
    product_id: string,
    product_size: string,
    quantity: number
}

const Delete_products = ({product_id, product_size, quantity}: IDelete_products) => {
    const router = useRouter()
    const {toast} = useToast()
  return (
      <span onClick={() => {
        deleteCart(product_id, product_size, quantity); 
        router.refresh();
        toast({
          title: "Product Remove from Cart",
          action: <ToastAction onClick={()=> {router.push("/")}} altText="Continue Shopping">Continue Shopping</ToastAction>,
        })}} className='text-gray-500 text-lg cursor-pointer' >x</span>
  )
}

export default Delete_products