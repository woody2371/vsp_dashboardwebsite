import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import sleepLogo from '@/images/sleep.png';
import DatePicker from 'react-datepicker';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';
import 'react-datepicker/dist/react-datepicker.css';
const Dashboard = ({ stateName }) => {
    const [pickData, setPickData] = useState({});
    const [commitData, setCommitData] = useState({});
    const [backorderData, setBackorderData] = useState({});
    const [lastUpdatedData, setLastUpdatedData] = useState({});
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [search, setSearch] = useState('');
    //Fetch data every 15000ms
    useEffect(() => {
        fetchAllData();
        const interval = setInterval(fetchAllData, 15000);
        return () => clearInterval(interval);
    }, [stateName]);
    const fetchAllData = async () => {
        try {
            const res = await fetch(`/api/dashboard/${stateName}`);
            const json = await res.json();
            setPickData(json.pickDict);
            setCommitData(json.commitDict);
            setBackorderData(json.backorderDict);
            setLastUpdatedData(json.lastUpdated);
        }
        catch (err) {
            console.error(err);
        }
    };
    //Menu bar
    const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
    function updateDaysOld(item) {
        /** Take `item` and update how old the last modification is, and apply a background colour to assist in formatting later */
        const modified = new Date(item.dateLastModified);
        const today = new Date();
        const diffTime = Math.abs(today.getTime() - modified.getTime());
        /** Figure out in days how long ago this was modified */
        item.daysOld = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        /** Set formatting based on age */
        if (item.daysOld > 30) {
            item.bg = 'bg-red-600 text-white';
        }
        else if (item.daysOld > 15) {
            item.bg = 'bg-yellow-400 text-black';
        }
        else {
            item.bg = 'bg-[#607d8b] text-white';
        }
        /** return entire item for use elsewhere */
        return item;
    }
    //Search functionality is defined here, and included later in each section's filter
    const globalFilter = (item) => Object.values(item).some(val => typeof val === 'string' && val.toLowerCase().includes(search.toLowerCase()));
    /** Function to ignore a row of data until a specified date. Equivalent previously was the sleep.datepicker() script */
    const sleepRow = async (salesOrder, productNum, selectedDate) => {
        const formattedDate = selectedDate.toLocaleDateString('en-GB').split('/').join('/'); // dd/mm/yyyy
        try {
            const params = new URLSearchParams({
                row: `${salesOrder},${productNum}`,
                dateUntil: formattedDate,
                state: stateName,
            });
            await fetch(`/api/delete_row?${params.toString()}`, { method: 'GET' });
            fetchAllData(); //Refresh data now that we've removed a line or lines
        }
        catch (error) {
            console.error('Error during sleep request:', error);
        }
    };
    return (_jsxs("div", { className: "flex h-screen", children: [_jsx("div", { className: `transition-all ease-in-out duration-500 bg-gray-800 text-white ${sidebarOpen ? 'w-[10%]' : 'w-0'} overflow-hidden`, children: _jsxs("div", { className: "p-4", children: [_jsx("h2", { className: "text-lg font-bold mb-4", children: "Navigation" }), _jsx(Button, { variant: "ghost", className: "w-full text-left", onClick: toggleSidebar, children: "Close" }), _jsx("a", { href: "/dashboard/WA", className: "block mt-2", children: "WA Dashboard" }), _jsx("a", { href: "/dashboard/QLD", className: "block mt-2", children: "QLD Dashboard" }), _jsx("a", { href: `/ignored_orders/${stateName}`, className: "block mt-2", children: "Ignored Orders" })] }) }), _jsxs("div", { className: "flex-1 p-0 overflow-y-auto", children: [_jsxs("div", { className: "bg-black text-white p-4 justify-between items-center flex-auto", children: [_jsx(Button, { variant: "outline", onClick: toggleSidebar, className: "ml-4 text-black", children: "Menu" }), _jsxs("h1", { className: "text-5xl text-center flex-1", children: ["VSP Dashboard - ", stateName.toUpperCase()] }), _jsxs("h6", { className: "text-center flex-1", children: [" Last Updated ", Object.values(lastUpdatedData)] }), _jsx("div", { className: "flex-1 text-right", children: _jsx(Input, { placeholder: "Search...", value: search, 
                                    // Dynamically update the filter based on what you enter in search
                                    onChange: (e) => setSearch(e.target.value), className: "w-64 inline-block text-black" }) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4 mt-4", children: [_jsx(Card, { children: _jsxs(CardContent, { className: "p-4 overflow-x-auto", children: [_jsx("h2", { className: "text-3xl font-semibold mb-4 text-center", children: "Outstanding Picks" }), _jsxs("table", { className: "w-full", children: [_jsx("thead", { className: "bg-black text-white", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2 text-left", children: "Sales Order Number" }), _jsx("th", { className: "p-2", children: "Qty to Pick" }), _jsx("th", { className: "p-2 text-left", colSpan: 2, children: "Qty in Stock" })] }) }), _jsx("tbody", { children: Object.entries(pickData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => (_jsxs(React.Fragment, { children: [_jsx("tr", { className: "bg-[#607d8b] text-white", children: _jsxs("td", { className: "p-2 text-lg font-semibold", colSpan: 4, children: [items[0]?.billToName, " - ", soNumber] }) }), items.map((item, idx) => (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 text-right text-base", children: item.productNum }), _jsx("td", { className: "p-2 bg-green-600 text-white text-center", children: item.qty }), _jsxs("td", { className: "p-2 text-center", children: [item.qtyonhand, " "] }), _jsx("td", { className: "p-2 text-center", children: _jsx(DatePicker, { selected: null, onChange: (date) => date && sleepRow(soNumber, item.productNum, date), customInput: _jsx("img", { src: sleepLogo, alt: "Sleep", className: "w-6 h-6 cursor-pointer inline", title: "Put to Sleep" //Wish putting my child to sleep was this easy
                                                                             }), popperPlacement: "bottom", dateFormat: "dd/MM/yyyy" //Australian made baby
                                                                            , showMonthDropdown: true, showYearDropdown: true, dropdownMode: "select" }) })] }, idx)))] }, soNumber))) })] })] }) }), _jsx(Card, { children: _jsxs(CardContent, { className: "p-4 overflow-x-auto", children: [_jsx("h2", { className: "text-3xl font-semibold mb-4 text-center", children: "Committed Sales" }), _jsxs("table", { className: "w-full text-base", children: [_jsx("thead", { className: "bg-black text-white", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2 text-left", children: "Sales Order Number" }), _jsx("th", { className: "p-2", children: "Qty Committed" })] }) }), _jsx("tbody", { children: Object.entries(commitData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => [soNumber, items.map(updateDaysOld)])
                                                        .sort(([, a], [, b]) => b[0].daysOld - a[0].daysOld).map(([soNumber, items]) => (_jsxs(React.Fragment, { children: [_jsxs("tr", { className: "bg-[#607d8b] text-white", children: [_jsxs("td", { className: "p-2 text-lg font-semibold", children: [items[0]?.billToName, " - ", soNumber] }), _jsxs("td", { className: `p-2 text-center font-semibold ${updateDaysOld(items[0]).bg}`, children: [updateDaysOld(items[0]).daysOld, " Days"] })] }), items.map((item, idx) => {
                                                                return (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 text-right", children: item.productNum }), _jsx("td", { className: "p-2 text-center bg-green-600 text-white text-center", children: item.qty })] }, idx));
                                                            })] }, soNumber))) })] })] }) })] }), _jsx("div", { className: "p-0", children: _jsx(Card, { children: _jsxs(CardContent, { className: "p-4 overflow-x-auto", children: [_jsx("h2", { className: "text-2xl font-semibold mb-4 text-center", children: "Backorders" }), _jsxs("table", { className: "w-full text-sm", children: [_jsx("thead", { className: "bg-black text-white", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2", children: "Product" }), _jsx("th", { className: "p-2", children: "Qty on Backorder" }), _jsx("th", { className: "p-2", children: "Qty on Order" }), _jsx("th", { className: "p-2", children: "Days Since Modified" }), _jsx("th", { className: "p-2", children: "Notes" })] }) }), _jsx("tbody", { children: Object.entries(Object.values(backorderData)
                                                    .flat()
                                                    .filter(globalFilter)
                                                    .reduce((acc, item) => {
                                                    if (!acc[item.productNum])
                                                        acc[item.productNum] = [];
                                                    acc[item.productNum].push(item);
                                                    return acc;
                                                }, {})).map(([productNum, items]) => {
                                                    const totalQty = items.reduce((sum, i) => sum + i.qty, 0);
                                                    const orderQty = parseInt(items[0].qtyonordertotal) || 0;
                                                    const needsRed = orderQty < totalQty;
                                                    const bgClass = needsRed ? 'bg-red-600 text-white' : 'bg-[#607d8b] text-white';
                                                    return (_jsxs(React.Fragment, { children: [_jsxs("tr", { className: "font-bold", children: [_jsx("td", { className: "p-2 bg-[#607d8b] text-white text-lg font-semibold", children: productNum }), _jsx("td", { className: `p-2 text-center ${bgClass}`, children: totalQty }), _jsx("td", { className: `p-2 text-center ${bgClass}`, children: orderQty }), _jsx("td", { className: "p-2 bg-[#607d8b] text-white" }), _jsx("td", { className: "p-2 bg-[#607d8b] text-white" })] }), items.map((item, idx) => {
                                                                const modified = new Date(item.dateLastModified);
                                                                const today = new Date();
                                                                const diffDays = Math.floor((+today - +modified) / (1000 * 60 * 60 * 24));
                                                                const daysText = diffDays === 0 ? 'Today' : `${diffDays} Days`;
                                                                return (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2", children: _jsxs(Popover, { children: [_jsxs(PopoverTrigger, { className: "cursor-pointer text-base w-full text-right block", children: [item.billToName, " - ", item.num] }), _jsxs(PopoverContent, { children: [_jsxs("p", { className: "font-bold mb-2", children: [item.billToName, " - ", item.num] }), _jsxs("table", { className: "text-base w-full", children: [_jsx("thead", { children: _jsxs("tr", { children: [_jsx("th", { className: "text-left", children: "Product" }), _jsx("th", { children: "Qty" }), _jsx("th", { children: "Status" })] }) }), _jsx("tbody", { children: (pickData[item.num] || []).map((line, i) => (_jsxs("tr", { children: [_jsx("td", { children: line.productNum }), _jsx("td", { className: "text-center", children: line.qty }), _jsx("td", { className: "text-center", children: line.pickItemstatusText || '-' })] }, i))) })] })] })] }) }), _jsx("td", { className: "p-2 text-center", children: item.qty }), _jsx("td", { className: "p-2 text-center", children: Math.trunc(parseInt(item.qtyonordertotal) || 0) }), _jsx("td", { className: "p-2 text-center", children: daysText }), _jsx("td", { className: "p-2 max-w-xs truncate", children: item.note || '' })] }, idx));
                                                            })] }, productNum));
                                                }) })] })] }) }) })] })] }));
};
export default Dashboard;
