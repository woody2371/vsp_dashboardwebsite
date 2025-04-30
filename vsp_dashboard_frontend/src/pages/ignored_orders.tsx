import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import 'react-datepicker/dist/react-datepicker.css';

// Types
interface ignored_ordersProps {
  stateName: string;
}

interface ignoreItem {
  so: string;
  product: string;
  date: string;
  state: string;
}

interface apiResponse {
  ignoreDict: Record<string, ignoreItem[]>;
}

const ignored_orders: React.FC<ignored_ordersProps> = ({ stateName }) => {
  const [ignoreData, setignoreData] = useState<Record<string, ignoreItem[]>>({});
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
      const json: apiResponse = await res.json();
      setignoreData(json.ignoreDict);
    } catch (err) {
      console.error(err);
    }
  };

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const globalFilter = (item: any) =>
    Object.values(item).some(
      val => typeof val === 'string' && val.toLowerCase().includes(search.toLowerCase())
    );

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className={`transition-all ease-in-out duration-500 bg-gray-800 text-white ${sidebarOpen ? 'w-[10%]' : 'w-0'} overflow-hidden`}>
        <div className="p-4">
          <h2 className="text-lg font-bold mb-4">Navigation</h2>
          <Button variant="ghost" className="w-full text-left" onClick={toggleSidebar}>Close</Button>
          <a href="/dashboard/WA" className="block mt-2">WA Dashboard</a>
          <a href="/dashboard/QLD" className="block mt-2">QLD Dashboard</a>
          <a href={`/ignored_orders/${stateName}`} className="block mt-2">Ignored Orders</a>
        {/** Not yet implemented <a href="/dell" className="block mt-2">Dell ETAs</a> */}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-0 overflow-y-auto">
        {/* Header */}
        <div className="bg-black text-white p-4 justify-between items-center flex-auto">
          <Button variant="outline" onClick={toggleSidebar} className="ml-4 text-black">
            Menu
          </Button>
          <h1 className="text-5xl text-center flex-1">VSP Ignored Orders - {stateName.toUpperCase()}</h1>
          <div className="flex-1 text-right">
            <Input
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64 inline-block text-black"
            />
          </div>
        </div>

        {/* Content */}
        <div className="grid mx-auto w-[60%]">
          {/* Ignored Orders */}
          <Card>
            <CardContent className="p-4 overflow-x-auto">
              <h2 className="text-3xl font-semibold mb-4 text-center">Ignored Orders</h2>
              <table className="w-full">
                <thead className="bg-black text-white">
                  <tr>
                    <th className="p-2 text-left">Sales Order Number</th>
                    <th className="p-2">Product</th>
                    <th className="p-2">Date Ignored Until</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(ignoreData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => (
                    <React.Fragment key={soNumber}>
                      {items.map((item, idx) => (
                        <tr key={idx} className="border-t">
                          <td className="p-2 text-center">{soNumber}</td>
                          <td className="p-2 text-center">{item.product}</td>
                          <td className="p-2 text-center">{item.date}</td>
                        </tr>
                      ))}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ignored_orders;