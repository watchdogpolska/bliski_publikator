// // import 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/from';
import 'rxjs/add/observable/throw';

import { enableProdMode} from '@angular/core';

import { AppModule }  from './app/app.module';

if ('prod' === ENV) {
  enableProdMode();
}

import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
platformBrowserDynamic().bootstrapModule(AppModule);