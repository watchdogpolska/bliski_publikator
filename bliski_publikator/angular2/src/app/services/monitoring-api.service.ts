import { Observable }     from 'rxjs/Observable';

import { Http } from 'angular2/http';

import { BaseApiService } from './api.base.service';
import { Monitoring } from '../model/monitoring';

import { QuestionBase } from '../model/question-base';
import { TextboxQuestion } from '../model/question-textbox';
import { DropdownQuestion } from '../model/question-dropdown';

import { isEqualConditional } from '../conditionals/conditional-is-equal'
import { isNullConditional } from '../conditionals/conditional-is-null'

import {CsrfService} from '../services/csrf.service';

export class MonitoringService extends BaseApiService {

    constructor(http: Http, csrf: CsrfService) {
        super(http, csrf);
    }

    saveMonitoring(monitoring: Monitoring){
        var data = monitoring.toPlainObject();
        return this.simple_post('monitoring/', data, {'url': document.location});
    }

    getMonitoring(id: number):Observable<Monitoring> {
        return this.simple_get(`monitoring/${id}`)
            .map(data => {
                let questions = this.parseQuestionsList(data.questions);
                this.addHideConditions(data.questions, questions);
                return new Monitoring(
                    {
                        name: data.name,
                        description: data.description,
                        questions: questions
                    }
                );
            })
            .map(data => data)
    }

    parseQuestionsList(questions:any[]):QuestionBase<any>[]{
        // console.log('parseQuestionsList', questions);
        return questions.map(this.parseQuestion)
    }

    parseQuestion(question):QuestionBase<any>{
        // console.log('parseQuestion', question);
        switch(question.type){
            case 'short_text':
                return new TextboxQuestion(question);
            case 'choice':
                return new DropdownQuestion(question);
        }
        throw new Error(`Unsupported controlType [${question.controlType}].`);
    }

    addHideConditions(data:any[], questions:QuestionBase<any>[]){
        var question_with_conditions = data.filter(t => t.hideConditions && t.hideConditions.length > 0);
        question_with_conditions.forEach( q => {
            var question = questions.find(t => t.id == q.id)
            question.hideConditions = q.hideConditions.map(c => this.parseHideConditions(c, questions))
        });
    }

    parseHideConditions(data, questions: QuestionBase<any>[]) {
        let target = questions[data.target];
        switch(data.type){
            case 'is-equal':{
                let value = data.value;
                return new isEqualConditional({ target, value });
            }
            case 'is-null':{
                return new isNullConditional({ target });
            }

        }
        throw new Error(`Unsupported hide conditions [${data.hideConditions}].`);
    }
}
