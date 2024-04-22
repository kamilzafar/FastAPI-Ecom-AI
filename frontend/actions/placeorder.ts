"use server"
import { myGetCookie } from "@/lib/auth"

interface IData {
    user: {
    firstname: string,
    lastname: string,
    address: string,
    state: string,
    city: string,
    contactnumber: string,
    paymentmethod: string
    }
}

export const placeorder = async (firstname: string, lastname: string, address: string, state: string,city: string,contactnumber: string, paymentmethod: string) => {
    const isCookies = await myGetCookie()  
    try{
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${isCookies}`
            },
            body: JSON.stringify(
                {
                    first_name: firstname,
                    last_name: lastname,
                    address: address,
                    state: state,
                    city: city,
                    contact_number: contactnumber,
                    payment_method: paymentmethod
                }
            )
        })        
        const data = await response.json()
        console.log(data, "data");
        return data
    }
    catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}