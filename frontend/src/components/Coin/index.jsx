import React from "react";

const Coin = ({ coin }) => {
	return (
		coin && (
			<>
				<div
					className="flex flex-wrap items-center justify-between w-full transition duration-500 ease-in-out transform bg-black border-2 border-gray-600 rounded-lg hover:border-white mb-3"
				>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 font-semibold tracking-widest text-white uppercase title-font">
								{coin?.coin_name}
							</h2>
						</div>
					</div>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 text-lg font-normal tracking-wide text-white">
								{coin?.price}
							</h2>
						</div>
					</div>
					<div className="w-full xl:w-1/4 md:w-1/4">
						<div className="relative flex flex-col h-full p-8 ">
							<h2 className="items-center mb-2 text-lg font-normal tracking-wide text-white uppercase">
								{coin?.currency_label}
							</h2>
						</div>
					</div>
				
				</div>
			</>
		)
	);
};

export default Coin;
