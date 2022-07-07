import Coin from "../Coin";
import React from "react";


const CoinTable = ({ coins }) => {

    return (
      <>
        <div className="container flex justify-center items-center mb-6">
          <div className="sections-list">
            {coins.length && (
              coins.map((coin) => (<Coin key={coin.price} coin={coin}  />))
              )}
            {!coins.length && (<p>No coins found!</p>)}
          </div>
        </div>
      </>
    )
}

export default CoinTable;