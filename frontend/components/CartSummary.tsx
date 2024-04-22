import { GetCart } from '@/actions/get_cart_product'
import { ICart } from '@/app/cart/page'
import React from 'react'

const CartSummary = async () => {
  const data: ICart[] = await GetCart() || []
  return (
    <div className='col-span-4 rounded-xl border'>
    <div className='flex justify-between items-center py-5 px-5'>
            <h2 className='text-xl font-bold'>Cart Summary</h2>
          </div>
          <div className='px-5 space-y-5'>
            {data ? (
              data.map((product, index) => {
                return (
                  <div key={product.product_data.sku} className='flex justify-between'>
                    <span>{product.product_data.name}</span>
                    <span>${product.product_data.price}</span>
                  </div>
                )
              })
            ) : (
              <div className='flex justify-between'>
                <span>No Product</span>
              </div>
            )}
            </div>
            <div className='border-t mt-5 px-5 py-5'>
              <div className='flex justify-between'>
                <span>Total</span>
                <span>Price</span>
              </div>
            </div>
            <div className='px-5 py-5'>
              <button className='w-full bg-black text-white py-2 rounded-lg'>Place Order</button>
            </div>
    </div>
    )
}

export default CartSummary