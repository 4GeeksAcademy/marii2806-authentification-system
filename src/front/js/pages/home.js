import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>Home Page</h1>
			<Link to="/signup">
					<button className="btn btn-primary">Signup</button>
			</Link>
			<Link to="/login">
					<button className="btn btn-primary">Login</button>
			</Link>
		</div>
	);
};
