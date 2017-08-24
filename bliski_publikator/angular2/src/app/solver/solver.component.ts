import {
    Component,
    Input,
    OnInit
} from '@angular/core';
import {
    FormBuilder,
    FormGroup,
    FormControl
} from '@angular/forms';
import { Monitoring } from '../model/monitoring';
import { QuestionBase } from '../model/question-base';
import { QuestionControlService } from './question-control.service';
import { AnswerService } from '../services/answers.service';

@Component({
    selector: 'sowp-solver',
    template: require('./solver.component.html'),
    // template: './question-solver.component.html',

})
export class SolverComponent implements OnInit {
    @Input()
    monitoring: Monitoring;

    form: FormGroup;
    visibility: { key:string, hidden:boolean }[] = [];


    constructor(private _fb: FormBuilder, private _api: AnswerService) {
        console.log(this._fb);
    }

    ngOnInit() {
        this.buildForm();
        this.observeFormValuesChanges();
    }

    onSubmit() {
        // let values = this.form.getRawValue();
        let values = this.form.value;
        
        if (!this.validateAnswer(values)) {
            alert('Sprawdz poprawność wypełnienia formularza');
            return;
        };
        this._api
            .saveAnswers(this.generateAnswerSheet(values))
            .subscribe(
                data => { console.log(data); document.location.href = data.return_url; },
                error => { console.log('FAIL', error); }
            );
    }
    
    observeFormValuesChanges() {
        this.form.valueChanges.forEach(console.log.bind(console));
        this.form.valueChanges.forEach((v) => this.validateVisibility(v));
        this.validateVisibility(this.form.value);
    }

    validateVisibility(values) {
        let questions = this.monitoring.questions;
        let visibility = [];
        questions.forEach(q => visibility.push({ key: q.key, hidden: q.isHidden(values) }) );
        this.visibility = visibility;
    }

    buildForm() {
        let group: any = {}
        this.monitoring.questions.forEach(t => group[t.key] = new FormControl(''));
        this.form = new FormGroup(group);
    }

    validateAnswer(values) {
        let questions = this.monitoring.questions;

        let list = Object.getOwnPropertyNames(values)
            .map(key => {
                return {
                    key: key,
                    value: values[key],
                    question: questions.find(q => q.key == key)
                };
            });
        let visible_list = list.filter(t => !t.question.isHidden(values));
        return visible_list.every(t => t.value != null)
            && visible_list.filter(t => typeof t == 'string').every(t => t.value.length > 0);
    }

    generateAnswerSheet(values) {
        console.log({ values });
        let questions = this.monitoring.questions;
        let answers = [];
        for (let answer_key in values) {
            let question = questions.find(q => q.key == answer_key);
            let curr_value = values[answer_key];
            answers.push({
                question_id: question.id,
                value: curr_value,
                point: question.calc_point_sum(curr_value)
            });
        }
        console.log({answers});
        return answers;
    }

    isHidden(question: QuestionBase<any>) {
        let o = this.visibility.find(t => t.key == question.key);
        if (!o) {
            return false;
        }
        return o.hidden;
    }
}
