import React, { useEffect, useState } from "react";
import { Link } from 'react-router-dom';
import FastAPIClient from "../../client";
import config from "../../config";
import DashboardHeader from "../../components/DashboardHeader";
import Footer from "../../components/Footer";
import jwtDecode from "jwt-decode";
import * as moment from "moment";
import CoinPriceTable from "../../components/CoinPriceTable";
import FormInput from "../../components/FormInput/FormInput";
import Button from "../../components/Button/Button";
import { NotLoggedIn } from "./NotLoggedIn";
import Loader from "../../components/Loader";
import PopupModal from "../../components/Modal/PopupModal";
import Select from "react-select";
//import Select from '../../components/Select';


const client = new FastAPIClient(config);

const optCoins = [
	{ value: 'bitcoin', label: 'Bitcoin' },
	{ value: 'ethereum', label: 'Ethereum' },
	{ value: 'bitcoin-cash', label: 'Bitcoin-cash' },
	{ value: 'litecoin', label: 'Litecoin' }
]

const optCurrencies = [
	{ value: 'usd', label: 'USD' },
	{ value: 'rub', label: 'RUB' },
	{ value: 'eur', label: 'EUR' }
]  

const ProfileView = ({ coinPrices }) => {
	return (
		<>
			<CoinPriceTable coinPrices={coinPrices}/>
		</>
	);
};

const CointrackDashboard = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [error, setError] = useState({ coin: "", currency: "", lower: "", upper: "" });
	const [followCoinForm, setFollowCoinForm] = useState({
		coin: "",
		currency: "",
		lower: 0.0,
		upper: 0.0,
	});

	const [showForm, setShowForm] = useState(false);
	const [coinPrices, setCoinPrices] = useState([]);

	const [loading, setLoading] = useState(false);
	const [refreshing, setRefreshing] = useState(true);

	useEffect(() => {
		fetchUserCoins();
	}, []);

	const fetchUserCoins = () => {
		client.getUserCoins().then(({ data }) => {
			setRefreshing(false);
			setCoinPrices(data);
		});
	};

    const limitValidation = (lower, upper) => {
          return lower < upper
        };

	const onFollowCoin = (e) => {
		e.preventDefault();
		setLoading(true);
		setError(false);

		if (followCoinForm.coin.length <= 0) {
			setLoading(false);
			return setError({ coin: "Please Choose Any Coin" });
		}
		if (followCoinForm.currency.length <= 0) {
			setLoading(false);
			return setError({ currency: "Please Choose Any Currency" });
		}
		if (followCoinForm.lower <= 0.0) {
			setLoading(false);
			return setError({ lower: "Please Enter Correct Lower Limit" });
		}
		if (isNaN(+followCoinForm.lower)) {
			setLoading(false);
			return setError({ lower: "Please Enter Whole Number Not String" });
		}
		if (followCoinForm.upper <= 0.0) {
			setLoading(false);
			return setError({ upper: "Please Enter Correct Upper Limit" });
		}
		if (isNaN(+followCoinForm.upper)) {
			setLoading(false);
			return setError({ upper: "Please Enter Whole Number Not String" });
		}
		if (!limitValidation(followCoinForm.lower, followCoinForm.upper)) {
			setLoading(false);
			console.log(typeof (followCoinForm.upper));
			return setError({ upper: "The upper limit should be greater than the lower" });
		}

		client.fetchUser().then((user) => {
			client
				.followCoin(
					followCoinForm.coin,
					followCoinForm.currency,
					followCoinForm.lower,
					followCoinForm.upper,
					user?.id
				)
				// eslint-disable-next-line no-unused-vars
				.then((data) => {  // eslint:ignore
					fetchUserCoins();
					setLoading(false);
					setShowForm(false);
				});
		});
	};

	useEffect(() => {
		const tokenString = localStorage.getItem("token");
		if (tokenString) {
			const token = JSON.parse(tokenString);
			const decodedAccessToken = jwtDecode(token.access_token);
			if (moment.unix(decodedAccessToken.exp).toDate() > new Date()) {
				setIsLoggedIn(true);
			}
		}
	}, []);

	if (refreshing) return !isLoggedIn ? <NotLoggedIn /> : <Loader />;

	return (
		<>
			<section
				className="flex flex-col bg-black text-center"
				style={{ minHeight: "100vh" }}
			>
				<DashboardHeader />
				<div className="container px-5 pt-6 text-center mx-auto lg:px-20">
					<h1 className="mb-12 text-3xl font-medium text-white">
						Cointrack - Better than you think. 
					</h1>

					<button
						className="my-5 text-white bg-teal-500 p-3 rounded"
						onClick={() => {
							setShowForm(!showForm);
						}}
					>
						Follow Coin
					</button>
					<p>
						<Link to="/my-coins" onClick={fetchUserCoins}
							className="text-base leading-relaxed text-white">Latest coins
						</Link>
					</p>
					<div className="mainViewport text-white">
						{coinPrices.length && (
							<ProfileView
								coinPrices={coinPrices}
							/>
						)}
					</div>
				</div>

				<Footer />
			</section>
			{showForm && (
				<PopupModal
					modalTitle={"Follow Coin Form"}
					onCloseBtnPress={() => {
						setShowForm(false);
						setError({ coin: "", currency: "", lower: "", upper: "" });
					}}
				>
					<div className="mt-4 text-left">
						<form className="mt-5" onSubmit={(e) => onFollowCoin(e)}>
						    <div name="chooseCoin">
                                <label className="block mb-2 text-teal-500" htmlFor="chooseCoin">Choose Any Coin</label>
							    <Select
								    options={optCoins}
								    className={`rounded w-full p-2 border-b-2 text-teal-700 outline-none focus:bg-gray-300`}
								    onChange={(e) =>
									    setFollowCoinForm({ ...followCoinForm, coin: e.value })
								    }
								/>
							</div>
							<div name="chooseCurrency">
                                <label className="block mb-2 text-teal-500" htmlFor="chooseCurrency">Choose Currency</label>
							    <Select
								    options={optCurrencies}
								    className={`rounded w-full p-2 border-b-2 text-teal-700 outline-none focus:bg-gray-300`}
								    onChange={(e) =>
									    setFollowCoinForm({ ...followCoinForm, currency: e.value })
								}
								/>
							</div>
							<FormInput
								type={"text"}
								name={"lower"}
								label={"Lower Limit"}
								error={error.lower}
								value={followCoinForm.lower}
								onChange={(e) =>
									setFollowCoinForm({ ...followCoinForm, lower: e.target.value })
								}
							/>
							<FormInput
								type={"text"}
								name={"upper"}
								label={"Upper Limit"}
								error={error.upper}
								value={followCoinForm.upper}
								onChange={(e) =>
									setFollowCoinForm({ ...followCoinForm, upper: e.target.value })
								}
							/>
							<Button
								loading={loading}
								error={error.upper}
								title={"Follow Coin"}
							/>
						</form>
					</div>
				</PopupModal>
			)}
		</>
	);
};

export default CointrackDashboard;
