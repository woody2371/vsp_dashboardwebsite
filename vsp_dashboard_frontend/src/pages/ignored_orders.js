import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import 'react-datepicker/dist/react-datepicker.css';
const ignored_orders = ({ stateName }) => {
    const [ignoreData, setignoreData] = useState({});
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [search, setSearch] = useState('');
    useEffect(() => {
        fetchAllData();
        const interval = setInterval(fetchAllData, 5000);
        return () => clearInterval(interval);
    }, [stateName]);
    const fetchAllData = async () => {
        try {
            const res = await fetch(`/api/ignored_orders/${stateName}`);
            const json = await res.json();
            setignoreData(json.ignoreDict);
        }
        catch (err) {
            console.error(err);
        }
    };
    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
    const globalFilter = (item) => Object.values(item).some(val => typeof val === 'string' && val.toLowerCase().includes(search.toLowerCase()));
    return (_jsxs("div", { className: "flex h-screen", children: [_jsx("div", { className: `transition-all ease-in-out duration-500 bg-gray-800 text-white ${sidebarOpen ? 'w-[10%]' : 'w-0'} overflow-hidden`, children: _jsxs("div", { className: "p-4", children: [_jsx("h2", { className: "text-lg font-bold mb-4", children: "Navigation" }), _jsx(Button, { variant: "ghost", className: "w-full text-left", onClick: toggleSidebar, children: "Close" }), _jsx("a", { href: "/dashboard/WA", className: "block mt-2", children: "WA Dashboard" }), _jsx("a", { href: "/dashboard/QLD", className: "block mt-2", children: "QLD Dashboard" }), _jsx("a", { href: `/ignored_orders/${stateName}`, className: "block mt-2", children: "Ignored Orders" })] }) }), _jsxs("div", { className: "flex-1 p-0 overflow-y-auto", children: [_jsxs("div", { className: "bg-black text-white p-4 justify-between items-center flex-auto", children: [_jsx(Button, { variant: "outline", onClick: toggleSidebar, className: "ml-4 text-black", children: "Menu" }), _jsxs("h1", { className: "text-5xl text-center flex-1", children: ["VSP Ignored Orders - ", stateName.toUpperCase()] }), _jsx("div", { className: "flex-1 text-right", children: _jsx(Input, { placeholder: "Search...", value: search, onChange: (e) => setSearch(e.target.value), className: "w-64 inline-block text-black" }) })] }), _jsx("div", { className: "grid mx-auto w-[60%]", children: _jsx(Card, { children: _jsxs(CardContent, { className: "p-4 overflow-x-auto", children: [_jsx("h2", { className: "text-3xl font-semibold mb-4 text-center", children: "Ignored Orders" }), _jsxs("table", { className: "w-full", children: [_jsx("thead", { className: "bg-black text-white", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2 text-left", children: "Sales Order Number" }), _jsx("th", { className: "p-2", children: "Product" }), _jsx("th", { className: "p-2", children: "Date Ignored Until" })] }) }), _jsx("tbody", { children: Object.entries(ignoreData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => (_jsx(React.Fragment, { children: items.map((item, idx) => (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 text-center", children: soNumber }), _jsx("td", { className: "p-2 text-center", children: item.product }), _jsx("td", { className: "p-2 text-center", children: item.date })] }, idx))) }, soNumber))) })] })] }) }) })] })] }));
};
export default ignored_orders;
