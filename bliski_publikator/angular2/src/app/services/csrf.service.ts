import { Injectable } from 'angular2/core';

@Injectable();
export class CsrfService{

	constructor() {}

	getToken() {
		return this.parseCookie()['csrftoken'];
	}

	private parseCookie() {
		return document.cookie
			.split(';')
			.map(t => t.split('='))
			.reduce((v, t) => { v[t[0]] = (t[1] || ''); return v }, {})
	}
}
