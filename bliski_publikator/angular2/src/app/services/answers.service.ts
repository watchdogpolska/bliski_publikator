import { DOCUMENT } from '@angular/common';
import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class AnswerService {

    constructor(
        private _http: HttpClient,
        @Inject(DOCUMENT) private _doc: any) {
    }

    saveAnswers(answers: { id: number, value: string, point: number }[]) {
        let result = answers;
        let point = answers.reduce((prev, curr) => prev + curr.point, 0);
        return this._http.post<any>(this._doc.location.pathname, {result, point});
    }
}
