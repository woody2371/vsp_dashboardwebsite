import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import { useParams } from 'react-router-dom';
import IgnoredOrders from './pages/ignored_orders';
function App() {
    return (_jsx(Router, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(Navigate, { to: "/dashboard/wa", replace: true }) }), _jsx(Route, { path: "/dashboard/:stateName", element: _jsx(DashboardWrapper, {}) }), _jsx(Route, { path: "/ignored_orders/:stateName", element: _jsx(IgnoredOrdersWrapper, {}) })] }) }));
}
// Wrap with URL param handling
const DashboardWrapper = () => {
    const { stateName } = useParams();
    return stateName ? _jsx(Dashboard, { stateName: stateName }) : _jsx("div", { children: "Loading..." });
};
const IgnoredOrdersWrapper = () => {
    const { stateName } = useParams();
    return stateName ? _jsx(IgnoredOrders, { stateName: stateName }) : _jsx("div", { children: "Loading..." });
};
export default App;
