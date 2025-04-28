import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';

// Types
interface DashboardProps {
  stateName: string;
}

interface PickItem {
  salesOrder?: string;
  productNum: string;
  qty: number;
  qtyonhand?: number;
  status?: string;
  num?: string;
  dateLastModified?: string;
  pickitemstatusText?: string;
}

interface CommitItem {
  salesOrder?: string;
  productNum: string;
  qty: number;
  dateLastModified?: string;
  num?: string;
}

interface BackorderItem {
  productNum: string;
  qty: number;
  qtyonordertotal?: string;
  note?: string;
  daysOld?: string;
  salesOrder?: string;
  num?: string;
  dateLastModified?: string;
  billToName?: string;
}

interface ApiResponse {
  pickDict: Record<string, PickItem[]>;
  commitDict: Record<string, CommitItem[]>;
  backorderDict: Record<string, BackorderItem[]>;
}

const Dashboard: React.FC<DashboardProps> = ({ stateName }) => {
  const [data, setData] = useState<ApiResponse>({
    pickDict: {},
    commitDict: {},
    backorderDict: {},
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({ pick: '', commit: '', backorder: '' });

  const [flattenedData, setFlattenedData] = useState({
    pickItems: [] as PickItem[],
    commitItems: [] as CommitItem[],
    backorderItems: [] as BackorderItem[],
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

      if (!json || typeof json !== 'object') throw new Error('Invalid API response');

      setData(json);
      setFlattenedData(flattenApiData(json));
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Error fetching data');
    } finally {
      setLoading(false);
    }
  };

  const flattenApiData = (apiData: ApiResponse) => {
    const pickItems: PickItem[] = [];
    const commitItems: CommitItem[] = [];
    const backorderItems: BackorderItem[] = [];

    Object.entries(apiData.pickDict).forEach(([orderNum, items]) => {
      items.forEach(item => pickItems.push({ ...item, salesOrder: orderNum }));
    });

    Object.values(apiData.commitDict).forEach(items => {
      if (Array.isArray(items)) commitItems.push(...items);
    });

    Object.entries(apiData.backorderDict).forEach(([productNum, items]) => {
      items.forEach(item => backorderItems.push({ ...item, productNum }));
    });

    return { pickItems, commitItems, backorderItems };
  };

  const filterList = <T extends Record<string, any>>(list: T[], filter: string): T[] => {
    return list.filter(item =>
      Object.values(item).some(
        val => val && typeof val === 'string' && val.toLowerCase().includes(filter.toLowerCase())
      )
    );
  };

  return (
    <div className="p-4 space-y-10 max-w-screen-2xl mx-auto">
      <header className="text-center">
        <h1 className="text-3xl font-bold tracking-wide text-gray-900">VSP Dashboard - {stateName}</h1>
        <p className="text-sm text-gray-500">Auto-refreshes every 5 seconds</p>
      </header>

      {error && <div className="text-red-500 bg-red-50 p-3 rounded">{error}</div>}
      {loading && <div className="text-center text-gray-500">Loading...</div>}

      <section>
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">Outstanding Picks</h2>
        <Input
          placeholder="Search picks..."
          value={filters.pick}
          onChange={(e) => setFilters({ ...filters, pick: e.target.value })}
          className="mb-3"
        />
        <Card>
          <CardContent className="overflow-x-auto">
            <table className="w-full text-sm border">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="p-2">Order</th>
                  <th className="p-2">Qty</th>
                  <th className="p-2">In Stock</th>
                  <th className="p-2">Product</th>
                  <th className="p-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {filterList(flattenedData.pickItems, filters.pick).map((item, i) => (
                  <tr key={i} className="border-t">
                    <td className="p-2 text-blue-700 font-semibold">{item.salesOrder}</td>
                    <td className="p-2 text-center text-green-700 font-medium">{item.qty}</td>
                    <td className="p-2 text-center">{item.qtyonhand ?? '-'}</td>
                    <td className="p-2">
                      <Popover>
                        <PopoverTrigger className="text-indigo-600 hover:underline cursor-pointer">
                          {item.productNum}
                        </PopoverTrigger>
                        <PopoverContent className="text-sm p-3 w-64">
                          <div>
                            <strong>Qty:</strong> {item.qty}<br />
                            <strong>Status:</strong> {item.pickitemstatusText || 'N/A'}<br />
                            <strong>Last Modified:</strong> {item.dateLastModified || 'N/A'}
                          </div>
                        </PopoverContent>
                      </Popover>
                    </td>
                    <td className="p-2">{item.pickitemstatusText || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </section>

      <section>
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">Committed Sales</h2>
        <Input
          placeholder="Search committed..."
          value={filters.commit}
          onChange={(e) => setFilters({ ...filters, commit: e.target.value })}
          className="mb-3"
        />
        <Card>
          <CardContent className="overflow-x-auto">
            <table className="w-full text-sm border">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="p-2">Order</th>
                  <th className="p-2">Qty</th>
                  <th className="p-2">Product</th>
                </tr>
              </thead>
              <tbody>
                {filterList(flattenedData.commitItems, filters.commit).map((item, i) => (
                  <tr key={i} className="border-t">
                    <td className="p-2 text-blue-700">{item.salesOrder}</td>
                    <td className="p-2 text-center text-green-700">{item.qty}</td>
                    <td className="p-2">{item.productNum}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </section>

      <section>
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">Backorders</h2>
        <Input
          placeholder="Search backorders..."
          value={filters.backorder}
          onChange={(e) => setFilters({ ...filters, backorder: e.target.value })}
          className="mb-3"
        />
        <Card>
          <CardContent className="overflow-x-auto">
            <table className="w-full text-sm border">
              <thead className="bg-gray-100 text-left">
                <tr>
                  <th className="p-2">Product</th>
                  <th className="p-2">Qty</th>
                  <th className="p-2">On Order</th>
                  <th className="p-2">Customer</th>
                  <th className="p-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {filterList(flattenedData.backorderItems, filters.backorder).map((item, i) => (
                  <tr key={i} className="border-t">
                    <td className="p-2 font-semibold text-blue-800">{item.productNum}</td>
                    <td className="p-2 text-center">{item.qty}</td>
                    <td className="p-2 text-center">{item.qtyonordertotal || '-'}</td>
                    <td className="p-2">{item.billToName || '-'}</td>
                    <td className="p-2">{item.dateLastModified ? new Date(item.dateLastModified).toLocaleDateString() : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </section>
    </div>
  );
};

export default Dashboard;
