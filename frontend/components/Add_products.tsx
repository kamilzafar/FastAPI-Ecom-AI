"use client"
import { addToCart } from "@/actions/add_to_cart"
import { useToast } from "@/components/ui/use-toast"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@/components/ui/toggle-group"
import { useRouter, useSearchParams } from "next/navigation"
import { IProducts } from "./Products"
import { ToastAction } from "./ui/toast"

const Product_to_Cart = ({product_data}: {product_data: IProducts}) => {
    const {toast} = useToast()
    const router = useRouter()
    const searchQuery = useSearchParams()
    const defaultSearchQuery = searchQuery?.get("size") ?? ""
    const quantity = 1

    const submitdata = () => {
        addToCart(defaultSearchQuery, product_data, quantity);
        toast({
            title: "Product Added to Cart",
            description: "Visit Cart to checkout",
            action: <ToastAction onClick={()=> router.push("/cart")} altText="View Cart">View Cart</ToastAction>,
          })
    }
    
  return (
    <div className='w-full h-min border basis-60 border-zinc-800 rounded bg-zinc-900'>
        <div className='flex flex-col justify-between gap-3 p-5 border-b border-zinc-800'>
            <h2 className='text-xl font-semibold'>{product_data.name}</h2>
            <span className='text-xl font-semibold'>${product_data.price}</span>
            <p className='mt-2 text-sm '>{product_data.description}</p>
        </div>
        <form onSubmit={submitdata}>
        <div className='py-5'>
        <ToggleGroup type='single' className='grid grid-cols-4 border-zinc-800 px-5 space-x-2.5 justify-center'>
            <ToggleGroupItem value='S' onClick={(e) => {router.push(`?size=S`)}} className='flex items-center hover:border-zinc-400 border-zinc-800 justify-center border px-1 py-1.5 bg-black rounded 
                transition duration-150 ease text-13'>
                    <span>S</span>
            </ToggleGroupItem>
            <ToggleGroupItem value='M' onClick={() => router.push(`?size=M`)} className='flex items-center hover:border-zinc-400 border-zinc-800 justify-center border px-1 py-1.5 bg-black rounded 
                transition duration-150 ease text-13'>
                    <span>M</span>
            </ToggleGroupItem>
            <ToggleGroupItem value='L' onClick={() => router.push(`?size=L`)} className='flex items-center hover:border-zinc-400 border-zinc-800 justify-center border px-1 py-1.5 bg-black rounded 
                transition duration-150 ease text-13 '>
                    <span>L</span>
            </ToggleGroupItem>
            <ToggleGroupItem value='XL' onClick={() => router.push("?size=XL")} className='flex items-center justify-center border hover:border-zinc-400 border-zinc-800 px-1 py-1.5 bg-black rounded 
                transition duration-150 ease text-13 '>
                    <span>XL</span>
            </ToggleGroupItem>
        </ToggleGroup>
        </div>
        <div className='border-t border-zinc-800 '>
            <button type="submit" className='w-full hover:bg-[#1F1F1F] border-zinc-800 p-2 transition duration-150 text-13 ease border'>Add to Cart</button>
        </div>
        </form>
    </div>
  )
}

export default Product_to_Cart