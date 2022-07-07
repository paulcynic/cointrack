import React, { useEffect, useState } from 'react';
import FastAPIClient from '../../client';
import config from '../../config';
import CoinTable from "../../components/CoinTable"
import DashboardHeader from "../../components/DashboardHeader";
import Footer from "../../components/Footer";
import Loader from '../../components/Loader';

const client = new FastAPIClient(config);


const Home = () => {

     const [loading, setLoading] = useState(true)
     const [coins, setCoins] = useState([])

     useEffect(() => {
          // FETCH THE COINS
          fetchCoins()
     }, [])


     const fetchCoins = () => {

          // SET THE LOADER TO TURE
          setLoading(true)

          // GET ALL COINS FROM THE API
          client.getCoins().then(({ data }) => {
               setLoading(false)

               // SET THE COINS DATA
               setCoins(data)
          });
     }


     if (loading)
          return <Loader />

     return (
          <>
               <section className="bg-black ">
                    <DashboardHeader />

                    <div className="container px-5 py-12 mx-auto lg:px-20">

                         <div className="flex flex-col flex-wrap pb-6 mb-12 text-white ">
                              <h1 className="mb-6 text-3xl font-medium text-white">
                                   Track your cryptocurrency with Cointrack!
                              </h1>
                              {/* <!-- This is an example component --> */}
                              <div className="container flex justify-center items-center mb-6">
                                   <button onClick={fetchCoins} className="h-10 w-20 text-white rounded bg-teal-500 hover:bg-teal-600">Show all</button>
                              </div>
                              {/* <p className="text-base leading-relaxed">
              Sample coins...</p> */}
                              <div className="mainViewport">
                                   <CoinTable
                                        coins={coins}
                                   />
                              </div>
                         </div>
                    </div>
                    <Footer />
               </section>
          </>
     )
}

export default Home;