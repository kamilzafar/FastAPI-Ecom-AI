import { GetCart } from '@/actions/get_cart_product'
import Link from 'next/link'
import Image from 'next/image'
import { IProducts } from '@/components/Products'
import ProductQuantity from '@/components/ProductQuantity'
import Delete_products from '@/components/Delete_products'
import { checkCookie } from '@/lib/auth'

export interface ICart {
  product_id: string,
  product_size: string,
  quantity: number,
  user_id: string,
  id: number,
  product_total: number,
  product_data: IProducts
}

const page = async () => {
  const isCookies = await checkCookie()
  if(isCookies){
  const data: ICart[] = await GetCart() || []
  if(data.length > 0){
  const price = data.reduce((acc, product) => acc + product.product_data.price*product.quantity, 0)
    return (
      <div className='lg:mx-20 md:mx-10 grid lg:grid-cols-3 mx-auto max-w-screen-2xl  md:grid-cols-2 grid-cols-1 md:space-y-6 space-y-9 space-x-5 md:space-x-10 '>
        {data.map((product, index) => {    
            const images = [product.product_data.image1, product.product_data.image2]
            return (
                <div key={product.product_data.sku} className='flex md:mt-6 md:ml-10 mt-9 ml-6 justify-between border border-solid border-zinc-800 rounded-md flex-col'>
                  <div className='overflow-hidden'>
                    <Image src={images[0]} alt={product.product_data.name} className='transition-transform duration-500 ease-in-out transform hover:scale-110' width={384} height={576} />
                  </div> 
                  <div className='flex justify-between relative flex-col p-3.5 z-10'>
                    <div className='flex justify-between items-center'>
                      <h3 className='font-semibold text-sm line-clamp-1'>{product.product_data.name}</h3>
                      <Delete_products product_id={product.product_id} product_size={product.product_size} quantity={product.quantity} />
                    </div>  
                      <p className='text-gray-500 text-sm mt-1'>${(product.product_data.price*product.quantity).toFixed(2)}</p>
                  </div>
                  <div className='flex items-center pb-3 justify-between mx-4'>
                    <ProductQuantity {...product} />
                    <span>{product.product_size}</span>
                  </div>
                </div>
            )
        })}
        <div className='fixed left-[50%] translate-x-[-50%] bottom-4 w-[90%] z-10 sm:w-[360px] rounded-xl overflow-hidden flex bg-black border border-solid h-min'>
          <div className="flex flex-col p-2.5 hover:bg-slate-800 justify-center w-1/2 gap-2 text-center">
            <div className='flex gap-2.5 justify-center text-sm'>
              <span>Total:</span>
              <span>{price.toFixed(2)}</span>
            </div>
              <span className='text-xs'>+ TAX INCL.</span>
          </div>
          <div className='w-1/2 border-l border-solid hover:bg-slate-800'>
            <Link href="/checkout">
              <button className='w-full h-full text-white '>
                Checkout
              </button>
            </Link>
          </div>
        </div>
      </div>
    )
  } else {
    return (
      <div className="flex flex-col mx-auto max-w-screen-2xl items-center justify-center w-full h-[calc(100vh-91px)] gap-2 px-4">
        <h1 className="mb-6 text-4xl font-bold">YOUR CART IS EMPTY</h1>
        <p className="mb-4 text-lg">When you have added something to your cart, it will appear here. Want to get started?</p>
        <Link
          className="flex font-medium	 items-center bg-[#0C0C0C] justify-center text-sm min-w-[160px] max-w-[160px] h-[40px] px-[10px] rounded-md border border-solid border-[#2E2E2E] transition-all hover:bg-[#1F1F1F] hover:border-[#454545]"
          href="/"
        >
          Start
        </Link>
      </div>
    )
  }
} else {
  return (
    <div className="flex flex-col items-center justify-center w-full h-[calc(100vh-91px)] gap-2 px-4">
      <h1 className="mb-6 text-4xl font-bold">YOUR CART IS EMPTY</h1>
      <p className="mb-4 text-lg">
        Not registered? You must be in order to save your products in the shopping cart.
      </p>
      <Link
        className="flex font-medium	 items-center bg-[#0C0C0C] justify-center text-sm min-w-[160px] max-w-[160px] h-[40px] px-[10px] rounded-md border border-solid border-[#2E2E2E] transition-all hover:bg-[#1F1F1F] hover:border-[#454545]"
        href="/login"
      >
        Login
      </Link>
    </div>
  );
}
}

export default page