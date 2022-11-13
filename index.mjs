import express from "express";
import morgan from "morgan";
import cryptoRandomString from "crypto-random-string";

const PORT = process.env.PORT ?? 3000;

const app = express();
app.use(morgan("combined"));

const generate = (l) => {
	const a = cryptoRandomString({ length: l, type: "alphanumeric" });
	const b = cryptoRandomString({ length: l, type: "distinguishable" });
	const c = cryptoRandomString({ length: l, type: "ascii-printable" });
	return `Random Stuff:\n${a}\n\nEasy to read:\n${b}\n\nPasswords:\n${c}\n\n`;
};

app.get("/:len(\\d{0,})", async (req, res) => {
	const len = parseInt(req.params.len, 10) || 32;
	res.send(generate(len > 128 ? 128 : len));
});

app.use((req, res) => {
	res.status(404).send("404 - File not found");
});

app.use((err, req, res, next) => {
	console.log(err);
	res.status(500).send("500 - Internal server error");
});

app.listen(PORT, () => console.log(`Server listening on port: ${PORT}`));
