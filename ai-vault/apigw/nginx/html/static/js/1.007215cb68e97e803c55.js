webpackJsonp([1],{HXef:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r=i("Xxa5"),n=i.n(r),a=i("exGp"),o=i.n(a),s=i("Dd8w"),c=i.n(s),l=i("lta2");function u(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};arguments.length>1&&void 0!==arguments[1]&&arguments[1];return Object(l.b)("/datamanager/v1/export",c()({},t),{responseType:"blob",signal:!1})}var h=i("y5xs"),d={name:"home",data:function(){return{useramount:0,datasize:0,version:"***",tableData:[],isAhealth:!0,isUhealth:!1,isDhealth:!1,tmpVersion:"",tmpTableData:[],tmpHealthStatus:!1,isQueryVersion:!1,isQueryCert:!1,isQueryHealth:!1,fileList:[],isConfirmUploading:!1,isUploading:!1,isDownloading:!1,mgmtcert:{CertType:"管理面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"},svccert:{CertType:"服务面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"}}},mounted:function(){this.fetchData()},methods:{handleGetUserAmount:function(){var t=this;Object(h.d)({},{}).then(function(e){"00000000"===e.data.status?(t.useramount=e.data.data.total,t.isUhealth=!0):(t.useramount=0,t.isUhealth=!1)})},handleGetDataSize:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(l.b)("/datamanager/v1/size",t,e)})({},{}).then(function(e){"00000000"===e.data.status?(t.datasize=(e.data.data.size/1024/1024).toFixed(2),t.isDhealth=!0):(t.datasize=0,t.isDhealth=!1)})},queryVersion:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(l.b)("/AIVAULT/v1/version/",t,e)})({},{}).then(function(e){"31000022"!==e.data.status&&(t.version=(e.data.data.version||"").split("_")[0],t.isQueryVersion=!0,t.queryHealth())})},queryHealth:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(l.b)("/AIVAULT/v1/health",t,e)})({},{}).then(function(e){"31000022"!==e.data.status&&(t.tmpHealthStatus=e.data.msg,"ok"===t.tmpHealthStatus?t.isAhealth=!0:t.isAhealth=!1,t.isQueryHealth=!0,t.queryCert())})},queryCert:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return Object(l.b)("/AIVAULT/v1/certStatus",t,e)})({},{}).then(function(e){"31000022"!==e.data.status&&(t.tableData=e.data.data,t.isQueryCert=!0,t.handleSpan())})},fetchData:function(){this.handleGetUserAmount(),this.handleGetDataSize(),this.queryVersion()},handleSpan:function(){var t=this,e=this.tableData.filter(function(t){return"MGMT"===t.CertType}),i=this.tableData.filter(function(t){return"MGMT"!==t.CertType});this.tableData=e.concat(i),this.tableData.forEach(function(e,i){"MGMT"===e.CertType&&(t.mgmtcert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.mgmtcert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.mgmtcert.CertValidDate=e.CertValidDate),t.svccert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.svccert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.svccert.CertValidDate=e.CertValidDate})},handleBeforeUpload:function(t){this.isUploading=!0;var e=t.type.indexOf("zip")>-1,i=t.size/1024/1024<=50;return e||(this.$message.error(this.$t("ERR_UPLOAD_FILE_TYPE")),this.isUploading=!1),i||(this.$message.error(this.$t("ERR_UPLOAD_FILE_SIZE")),this.isUploading=!1),e&&i},handleDownload:function(){var t=this;return o()(n.a.mark(function e(){var i,r,a,o,s;return n.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t.isDownloading=!0,e.next=3,u();case 3:i=e.sent,r=new Blob([i.data],{type:"application/zip"}),a=i.headers["content-disposition"].split(";")[1].split("=")[1],window.navigator&&window.navigator.msSaveOrOpenBlob?(window.navigator.msSaveBlob(r,a),console.log(1)):(o=window.URL||window.webkitURL||window.moxURL,(s=document.createElement("a")).href=o.createObjectURL(r),s.download=a,document.body.appendChild(s),s.click(),document.body.removeChild(s),window.URL.revokeObjectURL(o)),t.isDownloading=!1;case 8:case"end":return e.stop()}},e,t)}))()},handleUploadSuccess:function(t,e,i){"00000000"===t.status?this.$message.success({message:this.$t("SUCCESS_UPLOAD")}):this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.handleGetUserAmount(),this.isUploading=!1},handleUploadError:function(t,e,i){this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.isUploading=!1}}},v={render:function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"home"},[r("div",{staticClass:"left"},[r("div",{staticClass:"left-box first-left"},[r("div",{staticClass:"left-name"},[t._v(t._s(t.$t("USER_AMOUNT")))]),t._v(" "),r("div",{staticClass:"left-num"},[t._v(t._s(t.useramount))])]),t._v(" "),r("div",{staticClass:"left-box"},[r("div",{staticClass:"left-name"},[t._v(t._s(t.$t("SYS_DATA_SIZE")))]),t._v(" "),r("div",{staticClass:"left-num"},[t._v(t._s(t.datasize))])])]),t._v(" "),r("div",{staticClass:"right"},[r("div",{staticClass:"right-box right-top"},[r("div",[r("div",{staticClass:"title"},[t._v(t._s(t.$t("TOOL_INFO")))])]),t._v(" "),r("div",{staticClass:"top-button"},[r("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-upload2",loading:t.isUploading},on:{click:function(e){t.isConfirmUploading=!0}}},[t._v(t._s(t.$t("BUTTON_UPLOAD"))+"\n        ")]),t._v(" "),r("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-download",loading:t.isDownloading},on:{click:t.handleDownload}},[t._v(t._s(t.$t("BUTTON_DOWNLOAD"))+"\n        ")])],1),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("VERSION")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.version))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("HEALTH_STATUS")))]),t._v(" "),r("div",{staticClass:"health_info",staticStyle:{"margin-top":"5px"}},[this.isAhealth?r("div",{staticStyle:{display:"flex","flex-direction":"row"}},[r("img",{staticStyle:{margin:"8px"},attrs:{src:i("nwfx")}}),t._v(" "),r("div",{staticStyle:{"font-size":"20px","line-height":"30px","font-weight":"400","letter-spacing":"0",color:"#FFFFFE",margin:"8px"}},[t._v("\n              健康\n            ")])]):r("div",{staticStyle:{display:"flex","flex-direction":"row"}},[r("img",{staticStyle:{margin:"8px"},attrs:{src:i("vigF")}}),t._v(" "),r("div",{staticStyle:{"font-size":"20px","line-height":"30px","font-weight":"400","letter-spacing":"0",color:"#FFFFFE",margin:"0 8px"}},[t._v("\n              不健康\n            ")])])])])]),t._v(" "),r("div",{staticClass:"right-box"},[r("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertType))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertValidDate))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertAlarm))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CrlStatus))])])]),t._v(" "),r("div",{staticClass:"right-box"},[r("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertType))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertValidDate))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertAlarm))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CrlStatus))])])])]),t._v(" "),r("el-dialog",{attrs:{title:t.$t("UPLOAD_RISK"),visible:t.isConfirmUploading,width:"28%","close-on-click-modal":!1,modal:!1},on:{"update:visible":function(e){t.isConfirmUploading=e}}},[r("div",{staticClass:"dialog-tip"},[r("div",{staticStyle:{"margin-left":"16px","margin-right":"16px"}},[r("img",{attrs:{src:i("77VW")}})]),t._v("\n      "+t._s(t.$t("CONFIRM_UPLOAD_TIP"))+"\n    ")]),t._v(" "),r("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BTN_CANCEL")))]),t._v(" "),r("el-upload",{staticClass:"upload-demo",staticStyle:{display:"inline-block"},attrs:{action:"/datamanager/v1/import","file-list":t.fileList,"before-upload":t.handleBeforeUpload,"show-file-list":!1,"on-success":t.handleUploadSuccess,"on-error":t.handleUploadError}},[r("el-button",{directives:[{name:"no-more-click",rawName:"v-no-more-click"}],staticClass:"dialog-button",attrs:{type:"primary"},on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BUTTON_UPLOAD")))])],1)],1)])],1)},staticRenderFns:[]};var f=i("VU/8")(d,v,!1,function(t){i("jSNQ")},"data-v-2b991b3f",null);e.default=f.exports},SldL:function(t,e){!function(e){"use strict";var i,r=Object.prototype,n=r.hasOwnProperty,a="function"==typeof Symbol?Symbol:{},o=a.iterator||"@@iterator",s=a.asyncIterator||"@@asyncIterator",c=a.toStringTag||"@@toStringTag",l="object"==typeof t,u=e.regeneratorRuntime;if(u)l&&(t.exports=u);else{(u=e.regeneratorRuntime=l?t.exports:{}).wrap=C;var h="suspendedStart",d="suspendedYield",v="executing",f="completed",p={},_={};_[o]=function(){return this};var m=Object.getPrototypeOf,g=m&&m(m(D([])));g&&g!==r&&n.call(g,o)&&(_=g);var y=x.prototype=b.prototype=Object.create(_);L.prototype=y.constructor=x,x.constructor=L,x[c]=L.displayName="GeneratorFunction",u.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===L||"GeneratorFunction"===(e.displayName||e.name))},u.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,x):(t.__proto__=x,c in t||(t[c]="GeneratorFunction")),t.prototype=Object.create(y),t},u.awrap=function(t){return{__await:t}},U(E.prototype),E.prototype[s]=function(){return this},u.AsyncIterator=E,u.async=function(t,e,i,r){var n=new E(C(t,e,i,r));return u.isGeneratorFunction(e)?n:n.next().then(function(t){return t.done?t.value:n.next()})},U(y),y[c]="Generator",y[o]=function(){return this},y.toString=function(){return"[object Generator]"},u.keys=function(t){var e=[];for(var i in t)e.push(i);return e.reverse(),function i(){for(;e.length;){var r=e.pop();if(r in t)return i.value=r,i.done=!1,i}return i.done=!0,i}},u.values=D,A.prototype={constructor:A,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=i,this.done=!1,this.delegate=null,this.method="next",this.arg=i,this.tryEntries.forEach(T),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=i)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(r,n){return s.type="throw",s.arg=t,e.next=r,n&&(e.method="next",e.arg=i),!!n}for(var a=this.tryEntries.length-1;a>=0;--a){var o=this.tryEntries[a],s=o.completion;if("root"===o.tryLoc)return r("end");if(o.tryLoc<=this.prev){var c=n.call(o,"catchLoc"),l=n.call(o,"finallyLoc");if(c&&l){if(this.prev<o.catchLoc)return r(o.catchLoc,!0);if(this.prev<o.finallyLoc)return r(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return r(o.catchLoc,!0)}else{if(!l)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return r(o.finallyLoc)}}}},abrupt:function(t,e){for(var i=this.tryEntries.length-1;i>=0;--i){var r=this.tryEntries[i];if(r.tryLoc<=this.prev&&n.call(r,"finallyLoc")&&this.prev<r.finallyLoc){var a=r;break}}a&&("break"===t||"continue"===t)&&a.tryLoc<=e&&e<=a.finallyLoc&&(a=null);var o=a?a.completion:{};return o.type=t,o.arg=e,a?(this.method="next",this.next=a.finallyLoc,p):this.complete(o)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),p},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var i=this.tryEntries[e];if(i.finallyLoc===t)return this.complete(i.completion,i.afterLoc),T(i),p}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var i=this.tryEntries[e];if(i.tryLoc===t){var r=i.completion;if("throw"===r.type){var n=r.arg;T(i)}return n}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:D(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=i),p}}}function C(t,e,i,r){var n=e&&e.prototype instanceof b?e:b,a=Object.create(n.prototype),o=new A(r||[]);return a._invoke=function(t,e,i){var r=h;return function(n,a){if(r===v)throw new Error("Generator is already running");if(r===f){if("throw"===n)throw a;return R()}for(i.method=n,i.arg=a;;){var o=i.delegate;if(o){var s=S(o,i);if(s){if(s===p)continue;return s}}if("next"===i.method)i.sent=i._sent=i.arg;else if("throw"===i.method){if(r===h)throw r=f,i.arg;i.dispatchException(i.arg)}else"return"===i.method&&i.abrupt("return",i.arg);r=v;var c=w(t,e,i);if("normal"===c.type){if(r=i.done?f:d,c.arg===p)continue;return{value:c.arg,done:i.done}}"throw"===c.type&&(r=f,i.method="throw",i.arg=c.arg)}}}(t,i,o),a}function w(t,e,i){try{return{type:"normal",arg:t.call(e,i)}}catch(t){return{type:"throw",arg:t}}}function b(){}function L(){}function x(){}function U(t){["next","throw","return"].forEach(function(e){t[e]=function(t){return this._invoke(e,t)}})}function E(t){var e;this._invoke=function(i,r){function a(){return new Promise(function(e,a){!function e(i,r,a,o){var s=w(t[i],t,r);if("throw"!==s.type){var c=s.arg,l=c.value;return l&&"object"==typeof l&&n.call(l,"__await")?Promise.resolve(l.__await).then(function(t){e("next",t,a,o)},function(t){e("throw",t,a,o)}):Promise.resolve(l).then(function(t){c.value=t,a(c)},o)}o(s.arg)}(i,r,e,a)})}return e=e?e.then(a,a):a()}}function S(t,e){var r=t.iterator[e.method];if(r===i){if(e.delegate=null,"throw"===e.method){if(t.iterator.return&&(e.method="return",e.arg=i,S(t,e),"throw"===e.method))return p;e.method="throw",e.arg=new TypeError("The iterator does not provide a 'throw' method")}return p}var n=w(r,t.iterator,e.arg);if("throw"===n.type)return e.method="throw",e.arg=n.arg,e.delegate=null,p;var a=n.arg;return a?a.done?(e[t.resultName]=a.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=i),e.delegate=null,p):a:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,p)}function O(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function T(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function A(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(O,this),this.reset(!0)}function D(t){if(t){var e=t[o];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,a=function e(){for(;++r<t.length;)if(n.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=i,e.done=!0,e};return a.next=a}}return{next:R}}function R(){return{value:i,done:!0}}}(function(){return this}()||Function("return this")())},Xxa5:function(t,e,i){t.exports=i("jyFz")},exGp:function(t,e,i){"use strict";e.__esModule=!0;var r,n=i("//Fk"),a=(r=n)&&r.__esModule?r:{default:r};e.default=function(t){return function(){var e=t.apply(this,arguments);return new a.default(function(t,i){return function r(n,o){try{var s=e[n](o),c=s.value}catch(t){return void i(t)}if(!s.done)return a.default.resolve(c).then(function(t){r("next",t)},function(t){r("throw",t)});t(c)}("next")})}}},jSNQ:function(t,e){},jyFz:function(t,e,i){var r=function(){return this}()||Function("return this")(),n=r.regeneratorRuntime&&Object.getOwnPropertyNames(r).indexOf("regeneratorRuntime")>=0,a=n&&r.regeneratorRuntime;if(r.regeneratorRuntime=void 0,t.exports=i("SldL"),n)r.regeneratorRuntime=a;else try{delete r.regeneratorRuntime}catch(t){r.regeneratorRuntime=void 0}}});
//# sourceMappingURL=1.007215cb68e97e803c55.js.map