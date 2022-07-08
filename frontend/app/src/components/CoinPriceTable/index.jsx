import CoinPrice from "../CoinPrice";
import React from "react";


const CoinPriceTable = ({ coinPrices }) => {

    return (
      <>
          <div className="sections-list">
            {coinPrices.length && (
                coinPrices.map((coinPrice) => (<CoinPrice key={coinPrice.id} coinPrice={coinPrice}  />))
              )}
            {!coinPrices.length && (<p>No coins found!</p>)}
          </div>
      </>
    )
}

export default CoinPriceTable;