import Image from 'next/image'
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
  } from "@/components/ui/accordion"  
import { getProducts } from '@/actions/getProduct'
import { IProducts } from '@/components/Products'
import Product_to_Cart from '@/components/Add_products'
import { products } from '@/actions/products'

interface IPage{
    params : {
        slug: string
    }
}

const page = async ({params}: IPage) => {
    const product: IProducts = await getProducts(params.slug)
    const images = [product?.image1, product?.image2]
  return (
    <div className='mt-14 mb-10 mx-auto max-w-screen-2xl'>
        <div className='grid lg:grid-cols-2 gap-8 mx-10 shadow-lg rounded-lg'>
            <div className='flex justify-center space-x-1 lg:col-span-1'>
                {images.map((img, index) => {
                    return(
                        <div key={index} className='flex space-x-4'>
                            <Image src={img} alt={product.name} key={index} className='rounded-t-lg object-cover' width={850} height={1150} />
                        </div>
                    )
                }
        )}
            </div>
            <div className='lg:col-span-1'>
            <Product_to_Cart product_data={product}/>
            <Accordion type="single" className='py-5' collapsible>
                <AccordionItem value="item-1" className='border-zinc-800'>
                    <AccordionTrigger className='hover:no-underline'>Composition</AccordionTrigger>
                    <AccordionContent>
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2" className='border-zinc-800'>
                    <AccordionTrigger className='hover:no-underline'>Care</AccordionTrigger>
                    <AccordionContent>
                    Ratione nobis, voluptatum quia quis magnam repellat quibusdam qui! Rem quidem accusantium modi
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3" className='border-zinc-800'>
                    <AccordionTrigger className='hover:no-underline'>Origin</AccordionTrigger>
                    <AccordionContent>
                    rerum ipsa voluptatem dolorum. Esse numquam debitis officiis ipsam.
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
            </div>
        </div>
    </div>
  )
}

export default page

export const generateStaticParams = async () => {
    const fetchProducts = await products();

    return fetchProducts.map((product: IProducts) => ({
        slug: product.slug
    }))
}