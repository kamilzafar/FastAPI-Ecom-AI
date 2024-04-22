"use server"
export const products = async(search?: string) => {
  try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/products${search? `?query=${search}`: ""}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          cache: 'no-cache'
      })
      const data = await res.json()      
      return data
  }
  catch (error) {
      console.log(error, "error");
      console.log("error is error");
  }
}