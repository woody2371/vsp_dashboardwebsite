import { jsxs as _jsxs, jsx as _jsx } from "react/jsx-runtime";
import { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';
const Dashboard = ({ stateName }) => {
    const [data, setData] = useState({
        pickDict: {},
        commitDict: {},
        backorderDict: {},
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({ pick: '', commit: '', backorder: '' });
    const [flattenedData, setFlattenedData] = useState({
        pickItems: [],
        commitItems: [],
        backorderItems: [],
    });
    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);
        return () => clearInterval(interval);
    }, [stateName]);
    const fetchData = async () => {
        try {
            setLoading(true);
            const res = await fetch(`/api/${stateName}`);
            const json = await res.json();
            if (!json || typeof json !== 'object')
                throw new Error('Invalid API response');
            setData(json);
            setFlattenedData(flattenApiData(json));
            setError(null);
        }
        catch (err) {
            setError(err.message || 'Error fetching data');
        }
        finally {
            setLoading(false);
        }
    };
    const flattenApiData = (apiData) => {
        const pickItems = [];
        const commitItems = [];
        const backorderItems = [];
        Object.entries(apiData.pickDict).forEach(([orderNum, items]) => {
            items.forEach(item => pickItems.push({ ...item, salesOrder: orderNum }));
        });
        Object.values(apiData.commitDict).forEach(items => {
            if (Array.isArray(items))
                commitItems.push(...items);
        });
        Object.entries(apiData.backorderDict).forEach(([productNum, items]) => {
            items.forEach(item => backorderItems.push({ ...item, productNum }));
        });
        return { pickItems, commitItems, backorderItems };
    };
    const filterList = (list, filter) => {
        return list.filter(item => Object.values(item).some(val => val && typeof val === 'string' && val.toLowerCase().includes(filter.toLowerCase())));
    };
    return (_jsxs("div", { className: "p-4 space-y-10 max-w-screen-2xl mx-auto", children: [_jsxs("header", { className: "text-center", children: [_jsxs("h1", { className: "text-3xl font-bold tracking-wide text-gray-900", children: ["VSP Dashboard - ", stateName] }), _jsx("p", { className: "text-sm text-gray-500", children: "Auto-refreshes every 5 seconds" })] }), error && _jsx("div", { className: "text-red-500 bg-red-50 p-3 rounded", children: error }), loading && _jsx("div", { className: "text-center text-gray-500", children: "Loading..." }), _jsxs("section", { children: [_jsx("h2", { className: "text-2xl font-semibold text-gray-700 mb-2", children: "Outstanding Picks" }), _jsx(Input, { placeholder: "Search picks...", value: filters.pick, onChange: (e) => setFilters({ ...filters, pick: e.target.value }), className: "mb-3" }), _jsx(Card, { children: _jsx(CardContent, { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-sm border", children: [_jsx("thead", { className: "bg-gray-100 text-left", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2", children: "Order" }), _jsx("th", { className: "p-2", children: "Qty" }), _jsx("th", { className: "p-2", children: "In Stock" }), _jsx("th", { className: "p-2", children: "Product" }), _jsx("th", { className: "p-2", children: "Status" })] }) }), _jsx("tbody", { children: filterList(flattenedData.pickItems, filters.pick).map((item, i) => (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 text-blue-700 font-semibold", children: item.salesOrder }), _jsx("td", { className: "p-2 text-center text-green-700 font-medium", children: item.qty }), _jsx("td", { className: "p-2 text-center", children: item.qtyonhand ?? '-' }), _jsx("td", { className: "p-2", children: _jsxs(Popover, { children: [_jsx(PopoverTrigger, { className: "text-indigo-600 hover:underline cursor-pointer", children: item.productNum }), _jsx(PopoverContent, { className: "text-sm p-3 w-64", children: _jsxs("div", { children: [_jsx("strong", { children: "Qty:" }), " ", item.qty, _jsx("br", {}), _jsx("strong", { children: "Status:" }), " ", item.pickitemstatusText || 'N/A', _jsx("br", {}), _jsx("strong", { children: "Last Modified:" }), " ", item.dateLastModified || 'N/A'] }) })] }) }), _jsx("td", { className: "p-2", children: item.pickitemstatusText || '-' })] }, i))) })] }) }) })] }), _jsxs("section", { children: [_jsx("h2", { className: "text-2xl font-semibold text-gray-700 mb-2", children: "Committed Sales" }), _jsx(Input, { placeholder: "Search committed...", value: filters.commit, onChange: (e) => setFilters({ ...filters, commit: e.target.value }), className: "mb-3" }), _jsx(Card, { children: _jsx(CardContent, { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-sm border", children: [_jsx("thead", { className: "bg-gray-100 text-left", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2", children: "Order" }), _jsx("th", { className: "p-2", children: "Qty" }), _jsx("th", { className: "p-2", children: "Product" })] }) }), _jsx("tbody", { children: filterList(flattenedData.commitItems, filters.commit).map((item, i) => (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 text-blue-700", children: item.salesOrder }), _jsx("td", { className: "p-2 text-center text-green-700", children: item.qty }), _jsx("td", { className: "p-2", children: item.productNum })] }, i))) })] }) }) })] }), _jsxs("section", { children: [_jsx("h2", { className: "text-2xl font-semibold text-gray-700 mb-2", children: "Backorders" }), _jsx(Input, { placeholder: "Search backorders...", value: filters.backorder, onChange: (e) => setFilters({ ...filters, backorder: e.target.value }), className: "mb-3" }), _jsx(Card, { children: _jsx(CardContent, { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-sm border", children: [_jsx("thead", { className: "bg-gray-100 text-left", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2", children: "Product" }), _jsx("th", { className: "p-2", children: "Qty" }), _jsx("th", { className: "p-2", children: "On Order" }), _jsx("th", { className: "p-2", children: "Customer" }), _jsx("th", { className: "p-2", children: "Date" })] }) }), _jsx("tbody", { children: filterList(flattenedData.backorderItems, filters.backorder).map((item, i) => (_jsxs("tr", { className: "border-t", children: [_jsx("td", { className: "p-2 font-semibold text-blue-800", children: item.productNum }), _jsx("td", { className: "p-2 text-center", children: item.qty }), _jsx("td", { className: "p-2 text-center", children: item.qtyonordertotal || '-' }), _jsx("td", { className: "p-2", children: item.billToName || '-' }), _jsx("td", { className: "p-2", children: item.dateLastModified ? new Date(item.dateLastModified).toLocaleDateString() : '-' })] }, i))) })] }) }) })] })] }));
};
export default Dashboard;
