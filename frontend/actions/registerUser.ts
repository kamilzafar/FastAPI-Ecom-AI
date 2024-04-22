"use server"

export const registerUser = async (username: string, email: string, password: string) => {
    try{
    const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/signup`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        username: username,
        email: email,
        password: password,
        }),
    })
    const data = await response.json()
    return {"message": "User registered successfully"}
    } catch (error) {
        console.log(error, "error");
        console.log("error is error");
    }
}