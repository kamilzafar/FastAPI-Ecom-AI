"use client"
import { GetCart } from '@/actions/get_cart_product'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import Link from 'next/link'
import React, { FormEvent } from 'react'
import { useState, useEffect } from 'react'
import { ICart } from '../cart/page'
import Image from 'next/image'
import { placeorder } from '@/actions/placeorder'

const page = () => {
  const [paymentmethod, setPaymentMethod] = useState('cash')
  const [data, setData] = useState<ICart[]>([])
  const [firstname, setFirstname] = useState('')
  const [lastname, setLastname] = useState('')
  const [address, setAddress] = useState('')
  const [state, setState] = useState('')
  const [city, setCity] = useState('')
  const [contactnumber, setContactnumber] = useState('')
  useEffect(() => {
    const fetchData = async () => {
      const cart = await GetCart();
      setData(cart as ICart[]);
    }
    fetchData();
  }, [])

  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    placeorder(firstname, lastname, address, state, city, contactnumber, paymentmethod)
  };

  const price = data?.reduce((acc, item) => acc + item.product_data.price, 0)
  return (
    <form onSubmit={submit} className='grid mx-10  space-x-10 grid-cols-12 max-w-screen-2xl'>
        <div className='col-span-7 border px-5 rounded-xl'>
          <div className='flex py-5 justify-between items-center'>
            <h2 className='text-xl font-bold'>Checkout</h2>
            <span className='underline text-gray-500'>
              <Link href={"/cart"}>Back to Cart</Link>
            </span>
          </div>
          <h3 className='text-lg mb-4 font-semibold'>Billing Address</h3>
          {/* Customer Details */}
          <div className='space-y-5'>
            <div className='flex space-x-5'>
              <div className='flex-1 space-y-1'>
                <label htmlFor='firstName'>First Name</label>
                <input type='text' onChange={(e) => setFirstname(e.target.value)} id='firstname' name='firstname' placeholder='First Name' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
              <div className='flex-1 space-y-1'>
                <label htmlFor='lastName'>Last Name</label>
                <input type='text' id='lastname' onChange={(e)=> setLastname(e.target.value)} name='lastname' placeholder='Last Name' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
            </div>
            <div className='flex space-x-5'>
              <div className='flex-1 space-y-1'>
                <label htmlFor='address'>Address</label>
                <input type='text' id='address' name='address' onChange={(e)=> setAddress(e.target.value)} placeholder='Address' maxLength={40} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
              <div className='flex-1 space-y-1'>
                <label htmlFor='state'>State</label>
                <input type='text' id='state' name='state' placeholder='State' onChange={(e)=>setState(e.target.value)} maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
            </div>
            <div className='flex space-x-5'>
              <div className='flex-1 space-y-1'>
                <label htmlFor='city'>City</label>
                <input type='text' id='city' name='city' placeholder='City' onChange={(e)=> setCity(e.target.value)} maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
              <div className='flex-1 space-y-1'>
                <label htmlFor='contactnumber'>Contact Number</label>
                <input type='text' name='contactnumber' id='contactnumber' onChange={(e)=> setContactnumber(e.target.value)} placeholder='Contact Number' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
              </div>
            </div>
          </div>
          {/* Payment Methods */}
          <div className='mb-5 mt-10'>
            <h3 className='text-lg mb-4 font-semibold'>Payment Method</h3>
            <RadioGroup defaultValue="cash" onValueChange={(value:string)=>setPaymentMethod(value)}>
              <div className="flex items-center space-x-5">
                <div className='space-x-2'>
                  <RadioGroupItem value="cash" id="cash" />
                  <Label htmlFor="cash">Cash On Delivery</Label>
                </div>
                <div className='space-x-2'>
                  <RadioGroupItem value="card" id="card" />
                  <Label htmlFor="card">Card</Label>
                </div>
              </div>
            </RadioGroup>
            {paymentmethod == 'card' && (
              <div className='mt-5 space-y-5'>
                <h3 className='text-lg mb-4 font-semibold'>Card Details</h3>
                <div className='flex space-x-5'>
                  <div className='flex-1 space-y-1'>
                    <label htmlFor='cardNumber'>Card Number</label>
                    <input type='text' id='cardnumber' name='cardnumber' placeholder='Card Number' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
                  </div>
                  <div className='flex-1 space-y-1'>
                    <label htmlFor='expiryDate'>Expiry Date</label>
                    <input type='text' id='expirydate' name='expirydate' placeholder='Expiry Date' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
                  </div>
                </div>
                <div className='flex space-x-5'>
                  <div className='flex-1 space-y-1'>
                    <label htmlFor='cvv'>CVV</label>
                    <input type='text' name='cvv' id='cvv' placeholder='CVV' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
                  </div>
                  <div className='flex-1 space-y-1'>
                    <label htmlFor='cardName'>Card Name</label>
                    <input type='text' name='cardname' id='cardname' placeholder='Card Name' maxLength={20} minLength={5} className='w-full rounded-lg active:border p-2' />
                  </div>
                </div>
              </div> 
              )}
          </div>
        </div>
        {/* Cart Summary */}
        <div className='col-span-4 rounded-xl border'>
          <div className='flex justify-between items-center py-5 px-5'>
            <h2 className='text-xl font-bold'>Cart Summary</h2>
          </div>
          <div className='px-5 space-y-5'>
            {data?.length > 0 ? (
              data.map((product, index) => {
                return (
                  <div key={product.product_data.sku} className='flex space-x-3'>
                    <Image src={product.product_data.image1} alt={product.product_data.name} height={10} className='w-fit h-20 ' width={80} />
                    <span>{product.product_data.name}</span>
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
              <span>${price}</span>
            </div>
          </div>
          <div className='px-5 py-5'>
            <button type='submit' className='w-full bg-black text-white py-2 rounded-lg'>Place Order</button>
          </div>
        </div>
    </form>
  )
}

export default page