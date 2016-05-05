import { Injectable } from 'angular2/core';

@Injectable();
export class CsrfService{

	constructor() {}

	getToken() {
		let cookies = this.parseCookie();
		let r = cookies['csrftoken'];
		return r;
	}

	private parseCookie() {
		var cookies = {}
		document.cookie
			.split(';')
			.map(t => t.trim())
			.map(t => t.split('='))
			.forEach((t) => cookies[t[0]] = (t[1] || ''));
		return cookies;
	}
}
