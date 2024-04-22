import Products from "@/components/Products";

interface Props {
  searchParams: {
    search: string
  }
}

export default async function Home({searchParams}: Props) {    
  return (
    <main className="flex justify-center mx-auto max-w-screen-2xl">
      <Products search={searchParams.search}/>
    </main>
  );}

