"use client"
import React from 'react'
import { useRouter } from 'next/navigation'
import { useSearchParams } from 'next/navigation'
import { products } from '@/actions/products'

const Search = () => {
    const router = useRouter()
    const searchQuery = useSearchParams()
    const defaultSearchQuery = searchQuery?.get("search") ?? ""

    function onSubmit(event: React.FormEvent<HTMLFormElement>){
        event.preventDefault()
        const formData = new FormData(event.currentTarget)
        const searchQuery = formData.get("search")
        const search = async () => {
            const data = await products(defaultSearchQuery)
            return data
        }
        if (searchQuery) {
            router.replace(`/?search=${searchQuery}`)
            search()
        }
      }

  return (
    <form
    onSubmit={onSubmit}
    >
    <input
    id="search"
    name="search"
    type="search"
    placeholder='Search Product...' 
    className='py-2 px-6 hidden md:flex w-full bg-inherit border border-zinc-800 rounded-lg' 
    defaultValue={defaultSearchQuery}
    />   
    </form> 
  )
}

export default Search