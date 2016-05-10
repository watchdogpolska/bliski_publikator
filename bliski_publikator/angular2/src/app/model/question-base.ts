import { EventEmitter } from '@angular/core'

import { slugify } from '../utils';
import { BaseConditional } from '../conditionals/condititional-base';
import { BaseCountCondition } from '../count.conditions/cconditions.base';
import { Serializable } from '../serializable';

export class QuestionBase<T> {
    defaultValue: T;
    id: number;
    _key: string;
    name: string;
    description: string;
    order: number;
    controlType: string;
    private _hideConditions: BaseConditional[] = [];
    private _countConditions: BaseCountCondition[] = [];
    hideConditions_changes = new EventEmitter<BaseConditional[]>();
    countConditions_changes = new EventEmitter<BaseCountCondition[]>();

    constructor(options: {
        defaultValue?: T,
        id?: number,
        key?: string,
        name?: string,
        description?: string,
        order?: number,
        controlType?: string
    } = {}) {
        this.id = (options.id || options.id > 0) ? options.id : -1;
        this._key = options.key || '';
        this.name = options.name || '';
        this.description = options.description || '';
        this.order = options.order === undefined ? 1 : options.order;
        this.controlType = options.controlType || '';    }

    get key(){
        if (this._key)
            return this._key;
        this._key = slugify(this.name) + ( ( Math.random() * 1000 ) | 0)
        return this._key;
    }

    set key(value){
        this._key = value;
    }

    get hideConditions(){
        return this._hideConditions;
    }

    set hideConditions(conditions:BaseConditional[]) {
        this._hideConditions = conditions;
        this.hideConditions_changes.emit(conditions);
    }

    get countConditions(){
        return this._countConditions;
    }

    set countConditions(conditions: BaseCountCondition[]) {
        this._countConditions = conditions;
        this.countConditions_changes.emit(conditions);
    }

    get max_point_sum(){
        return this._countConditions
            .reduce((prev, curr) => prev + curr.point, 0);
    }

    calc_point_sum(answer) {
        return this._countConditions
            .filter(t => t.isValid(answer))
            .reduce((prev, curr) => prev + curr.point, 0);
    }

    isHidden(answers:any){
        if (this.hideConditions.length == 0)
            return false;
        return this.hideConditions.some(t => t.isValid(answers));
    }

    toPlainObject(questions: QuestionBase<any>[]) {
        let obj = {};
        if(this.id > 0){
            obj[ 'id' ] = this.id;
        }
        obj['name'] = this.name;
        obj['description'] = this.description;
        obj['order'] = this.order;
        obj['type'] = this.controlType;
        obj['defaultValue'] = this.defaultValue;
        obj['hideConditions'] = this._hideConditions.map(t => t.toPlainObject(questions));
        obj['countConditions'] = this._countConditions.map(t => t.toPlainObject());
        return obj;
    }
}
