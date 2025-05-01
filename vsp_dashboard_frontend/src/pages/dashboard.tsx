import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import sleepLogo from '@/images/sleep.png'
import DatePicker from 'react-datepicker';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover'; 
import 'react-datepicker/dist/react-datepicker.css';

// Types
interface dashboardProps {
  stateName: string;
}

//Outstanding items to be picked. Some of these aren't currently used (like status)
interface pickItem {
  salesOrder: string;
  billToName: string;
  productNum: string;
  qty: number;
  qtyonhand: number;
  status: string;
  num: string;
  dateLastModified: string;
  pickItemstatusText?: string;
}

//Items committed in full
interface commitItem {
  salesOrder: string;
  productNum: string;
  billToName: string;
  qty: number;
  dateLastModified: string;
  num: string;
  daysOld: number;
  bg: string;
}

//Items on backorder
interface backorderItem {
  productNum: string;
  qty: number;
  qtyonordertotal: string;
  note?: string;
  daysOld: string;
  salesOrder: string;
  num: string;
  dateLastModified: string;
  billToName: string;
}

//When was the data last updated
interface lastUpdated {
  lastUpdated: string;
}

//Used in our API calls later to pull the data from our flask app
interface apiResponse {
  pickDict: Record<string, pickItem[]>;
  commitDict: Record<string, commitItem[]>;
  backorderDict: Record<string, backorderItem[]>;
  lastUpdated: Record<string, lastUpdated[]>;
}

const Dashboard: React.FC<dashboardProps> = ({ stateName }) => {
  const [pickData, setPickData] = useState<Record<string, pickItem[]>>({});
  const [commitData, setCommitData] = useState<Record<string, commitItem[]>>({});
  const [backorderData, setBackorderData] = useState<Record<string, backorderItem[]>>({});
  const [lastUpdatedData, setLastUpdatedData] = useState<Record<string, lastUpdated[]>>({});
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
      const res = await fetch(`/api/dashboard/${stateName.toUpperCase()}`);
      const json: apiResponse = await res.json();
      setPickData(json.pickDict);
      setCommitData(json.commitDict);
      setBackorderData(json.backorderDict);
      setLastUpdatedData(json.lastUpdated);
    } catch (err) {
      console.error(err);
    }
  };

  //Menu bar
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  function updateDaysOld(item: commitItem): commitItem {
    /** Take `item` and update how old the last modification is, and apply a background colour to assist in formatting later */
    const modified = new Date(item.dateLastModified);
    const today = new Date();
    const diffTime = Math.abs(today.getTime() - modified.getTime());
    /** Figure out in days how long ago this was modified */
    item.daysOld = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    /** Set formatting based on age */
    if (item.daysOld > 30) {
      item.bg = 'bg-red-600 text-white';
    } else if (item.daysOld > 15) {
      item.bg = 'bg-yellow-400 text-black';
    } else {
      item.bg = 'bg-[#607d8b] text-white';
    }
    /** return entire item for use elsewhere */
    return item;
  }

  //Search functionality is defined here, and included later in each section's filter
  const globalFilter = (item: any) =>
    Object.values(item).some(
      val => typeof val === 'string' && val.toLowerCase().includes(search.toLowerCase())
    );
  
  /** Function to ignore a row of data until a specified date. Equivalent previously was the sleep.datepicker() script */
  const sleepRow = async (salesOrder: string, productNum: string, selectedDate: Date) => {
    const formattedDate = selectedDate.toLocaleDateString('en-GB').split('/').join('/'); // dd/mm/yyyy
    try {
      const params = new URLSearchParams({
        row: `${salesOrder},${productNum}`,
        dateUntil: formattedDate,
        state: stateName,
      });
      await fetch(`/api/delete_row?${params.toString()}`, { method: 'GET' });
      fetchAllData(); //Refresh data now that we've removed a line or lines
    } catch (error) {
      console.error('Error during sleep request:', error);
    }
  };

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
          <h1 className="text-5xl text-center flex-1">VSP Dashboard - {stateName.toUpperCase()}</h1>
          <h6 className="text-center flex-1"> Last Updated {Object.values(lastUpdatedData)}</h6>
          <div className="flex-1 text-right">
            <Input
              placeholder="Search..."
              value={search}
              // Dynamically update the filter based on what you enter in search
              onChange={(e) => setSearch(e.target.value)}
              className="w-64 inline-block text-black"
            />
          </div>
        </div>

        {/* Content */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          {/* Outstanding Picks */}
          <Card>
            <CardContent className="p-4 overflow-x-auto">
              <h2 className="text-3xl font-semibold mb-4 text-center">Outstanding Picks</h2>
              <table className="w-full">
                <thead className="bg-black text-white">
                  <tr>
                    <th className="p-2 text-left">Sales Order Number</th>
                    <th className="p-2">Qty to Pick</th>
                    <th className="p-2 text-left" colSpan={2}>Qty in Stock</th>
                  </tr>
                </thead>
                <tbody>
                  {/** Fill outstanding picks based on our search filter and the API data response */}
                  {Object.entries(pickData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => (
                    <React.Fragment key={soNumber}>
                      <tr className="bg-[#607d8b] text-white">
                        <td className="p-2 text-lg font-semibold" colSpan={4}>{items[0]?.billToName} - {soNumber}</td>
                      </tr>
                      {items.map((item, idx) => (
                        <tr key={idx} className="border-t">
                          <td className="p-2 text-right text-base">{item.productNum}</td>
                          <td className="p-2 bg-green-600 text-white text-center">{item.qty}</td>
                          <td className="p-2 text-center">{item.qtyonhand} </td>
                          <td className="p-2 text-center">
                            {/** Sleep functionality - logo with a calendar popover that sends a GET request back to our API backend */}
                            <DatePicker
                              selected={null}
                              onChange={(date) => date && sleepRow(soNumber, item.productNum, date)}
                              customInput={
                                <img
                                  src={sleepLogo}
                                  alt="Sleep"
                                  className="w-6 h-6 cursor-pointer inline"
                                  title="Put to Sleep" //Wish putting my child to sleep was this easy
                                />
                              }
                              popperPlacement="bottom"
                              dateFormat="dd/MM/yyyy" //Australian made baby
                              showMonthDropdown
                              showYearDropdown
                              dropdownMode="select"
                            />
                        </td>
                        </tr>
                      ))}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>

          {/** Committed Sales */}
          <Card>
            <CardContent className="p-4 overflow-x-auto">
              <h2 className="text-3xl font-semibold mb-4 text-center">Committed Sales</h2>
              <table className="w-full text-base">
                <thead className="bg-black text-white">
                  <tr>
                    <th className="p-2 text-left">Sales Order Number</th>
                    <th className="p-2">Qty Committed</th>
                  </tr>
                </thead>
                <tbody>
                {Object.entries(commitData).filter(([_, items]) => items.some(globalFilter)).map(([soNumber, items]) => [soNumber, items.map(updateDaysOld)] as [string, commitItem[]])
                          .sort(([, a], [, b]) => b[0].daysOld - a[0].daysOld).map(([soNumber, items]) => (
                    <React.Fragment key={soNumber}>
                      <tr className="bg-[#607d8b] text-white">
                        <td className="p-2 text-lg font-semibold">{items[0]?.billToName} - {soNumber}</td>
                        <td className={`p-2 text-center font-semibold ${updateDaysOld(items[0]).bg}`}>{updateDaysOld(items[0]).daysOld} Days</td>
                      </tr>
                      {items.map((item, idx) => {
                        return (
                          <tr key={idx} className="border-t">
                            <td className="p-2 text-right">{item.productNum}</td>
                            <td className="p-2 text-center bg-green-600 text-white text-center">{item.qty}</td>
                          </tr>
                        );
                      })}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
        </div>

          {/* Backorders */}
          <div className="p-0">
            <Card>
              <CardContent className="p-4 overflow-x-auto">
                <h2 className="text-2xl font-semibold mb-4 text-center">Backorders</h2>
                <table className="w-full text-sm">
                  <thead className="bg-black text-white">
                    <tr>
                      <th className="p-2">Product</th>
                      <th className="p-2">Qty on Backorder</th>
                      <th className="p-2">Qty on Order</th>
                      <th className="p-2">Days Since Modified</th>
                      <th className="p-2">Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(
                      Object.values(backorderData)
                        .flat()
                        .filter(globalFilter)
                        .reduce((acc, item) => {
                          if (!acc[item.productNum]) acc[item.productNum] = [];
                          acc[item.productNum].push(item);
                          return acc;
                        }, {} as Record<string, backorderItem[]>)
                    ).map(([productNum, items]) => {
                      const totalQty = items.reduce((sum, i) => sum + i.qty, 0);
                      const orderQty = parseInt(items[0].qtyonordertotal) || 0;
                      const needsRed = orderQty < totalQty;
                      const bgClass = needsRed ? 'bg-red-600 text-white' : 'bg-[#607d8b] text-white';

                      return (
                        <React.Fragment key={productNum}>
                          <tr className="font-bold">
                            <td className="p-2 bg-[#607d8b] text-white text-lg font-semibold">{productNum}</td>
                            <td className={`p-2 text-center ${bgClass}`}>{totalQty}</td>
                            <td className={`p-2 text-center ${bgClass}`}>{orderQty}</td>
                            <td className="p-2 bg-[#607d8b] text-white"></td>
                            <td className="p-2 bg-[#607d8b] text-white"></td>
                          </tr>
                          {items.map((item, idx) => {
                            const modified = new Date(item.dateLastModified);
                            const today = new Date();
                            const diffDays = Math.floor((+today - +modified) / (1000 * 60 * 60 * 24));
                            const daysText = diffDays === 0 ? 'Today' : `${diffDays} Days`;

                            return (
                              <tr key={idx} className="border-t">
                                <td className="p-2">
                                  <Popover>
                                    <PopoverTrigger className="cursor-pointer text-base w-full text-right block">
                                      {item.billToName} - {item.num}
                                    </PopoverTrigger>
                                    <PopoverContent>
                                      <p className="font-bold mb-2">{item.billToName} - {item.num}</p>
                                      <table className="text-base w-full">
                                        <thead>
                                          <tr>
                                            <th className="text-left">Product</th>
                                            <th>Qty</th>
                                            <th>Status</th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          {(pickData[item.num] || []).map((line, i) => (
                                            <tr key={i}>
                                              <td>{line.productNum}</td>
                                              <td className="text-center">{line.qty}</td>
                                              <td className="text-center">{line.pickItemstatusText || '-'}</td>
                                            </tr>
                                          ))}
                                        </tbody>
                                      </table>
                                    </PopoverContent>
                                  </Popover>
                                </td>
                                <td className="p-2 text-center">{item.qty}</td>
                                <td className="p-2 text-center">{Math.trunc(parseInt(item.qtyonordertotal) || 0)}</td>
                                <td className="p-2 text-center">{daysText}</td>
                                <td className="p-2 max-w-xs truncate">{item.note || ''}</td>
                              </tr>
                            );
                          })}
                        </React.Fragment>
                      );
                    })}
                  </tbody>
                </table>
              </CardContent>
            </Card>
          </div>
      </div>
    </div>
  );
};

export default Dashboard;