import React from "react";
import * as moment from "moment";

const CoinPrice = ({ coinPrice }) => {
	return (
		coinPrice && (
			<>
				<div
					className="flex flex-wrap items-center justify-between w-full transition duration-500 ease-in-out transform bg-black border-2 border-gray-600 rounded-lg hover:border-white mb-3"
				>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 font-semibold tracking-widest text-white uppercase title-font">
								{coinPrice?.coin_name}
							</h2>
						</div>
					</div>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 text-lg font-normal tracking-wide text-white">
								{coinPrice?.price}
							</h2>
						</div>
					</div>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 text-lg font-normal tracking-wide text-white uppercase">
								{coinPrice?.currency_label}
							</h2>
						</div>
					</div>
                    <div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 text-lg font-normal tracking-wide text-white">
								{moment(coinPrice?.current_datetime).format('DD-MM-YY HH:mm')}
							</h2>
						</div>
					</div>
				</div>
			</>
		)
	);
};

export default CoinPrice;