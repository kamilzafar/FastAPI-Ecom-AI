"use server"
import { userOrders } from "@/actions/getOrder"
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { checkCookie } from "@/lib/auth"
import Link from "next/link";

interface IOrders {
    id: number;
    first_name: string;
    last_name: string;
    address: string;
    city: string;
    state: string;
    contact_number: string;
    payment_method: string;
    order_date: string;
    order_total: number;
    order_status: string;
    user_id: string;
}  

const TableDemo = async () => {
    const isCookies = await checkCookie()
    if(isCookies){
    const orders: IOrders[] = await userOrders()

    if(orders.length > 0){
    const totalAmount = orders.reduce((acc, order) => acc + order.order_total, 0)
        return(
    <Table className="w-full mx-auto max-w-screen-2xl">
        <TableCaption>A list of your recent orders.</TableCaption>
        <TableHeader>
            <TableRow>
            <TableHead className="w-[100px]">Orders</TableHead>
            <TableHead>First Name</TableHead>
            <TableHead>Last Name</TableHead>
            <TableHead>Method</TableHead>
            <TableHead>Address</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Contact Number</TableHead>
            <TableHead className="text-right ">Amount</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            {orders.map((order) => (
            <TableRow key={order.id}>
                <TableCell className="font-medium">{order.id}</TableCell>
                <TableCell>{order.first_name}</TableCell>
                <TableCell>{order.last_name}</TableCell>
                <TableCell>{order.payment_method}</TableCell>
                <TableCell>{order.address}, {order.city}, {order.state}</TableCell>
                <TableCell>{order. order_status}</TableCell>
                <TableCell className="text-right">{order.contact_number}</TableCell>
                <TableCell className="text-right">{order.order_total}</TableCell>
            </TableRow>
            ))}
        </TableBody>
        <TableFooter>
            <TableRow>
            <TableCell colSpan={7}>Total</TableCell>
            <TableCell className="text-right">{totalAmount}</TableCell>
            </TableRow>
        </TableFooter>
    </Table>
    )} else {
        return (
            <div className="flex flex-col items-center justify-center w-full h-[80vh] gap-2 px-4">
                <h2 className="mb-6 text-4xl font-bold">NO ORDERS YET</h2>
                <p className="mb-4 text-lg">To create an order add a product to the cart and buy it!</p>
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
    return <div className="flex flex-col mx-auto max-w-screen-2xl items-center justify-center h-[calc(100vh-91px)] gap-2 px-4">
    <h2 className="mb-6 text-4xl font-bold">NO ORDERS YET</h2>
    <p className="mb-4 text-lg">To view your orders you must be logged in.</p>
    <Link
        className="flex font-medium	 items-center bg-[#0C0C0C] justify-center text-sm min-w-[160px] max-w-[160px] h-[40px] px-[10px] rounded-md border border-solid border-[#2E2E2E] transition-all hover:bg-[#1F1F1F] hover:border-[#454545]"
        href="/login"
    >
        Login
    </Link>
</div>
}
}

export default TableDemo