"use client"
import { updateCart } from '@/actions/updateCart'
import { ICart } from '@/app/cart/page'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

const ProductQuantity = (product: ICart) => {
    const router = useRouter()
    let [quantity, setQuantity] = useState(product.quantity)    
  return (
     <div className='flex bg-black w-min'> 
        <button id='minus' onClick={() => {setQuantity((previos) => previos-1);updateCart(product.product_id, product.product_size, quantity); router.refresh()}} className='flex items-center justify-center w-8 h-8 p-2 border border-solid rounded-l border-border-primary '>-</button>
        <span className='flex items-center justify-center w-8 h-8 p-2 border border-solid border-border-primary'>{quantity}</span>
        <button id='plus' onClick={()=> {setQuantity((previos) => previos+1);updateCart(product.product_id, product.product_size, quantity); router.refresh()}} className='flex items-center justify-center w-8 h-8 p-2 border border-solid rounded-r border-border-primary'>+</button>
      </div> 
  )
}

export default ProductQuantity