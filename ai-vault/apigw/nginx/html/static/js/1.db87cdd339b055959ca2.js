webpackJsonp([1],{HXef:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r=i("Xxa5"),n=i.n(r),a=i("exGp"),s=i.n(a),o=i("Dd8w"),l=i.n(o),c=i("lta2");function u(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(c.b)("/datamanager/v1/export",l()({},t),{responseType:"blob"})}var h=i("y5xs"),f={name:"home",data:function(){return{useramount:0,datasize:0,version:"***",tableData:[],isAhealth:!1,isUhealth:!1,isDhealth:!1,tmpVersion:"",tmpTableData:[],tmpHealthStatus:"",isQueryVersion:!1,isQueryCert:!1,isQueryHealth:!1,fileList:[],isConfirmUploading:!1,isUploading:!1,isDownloading:!1,mgmtcert:{CertType:"管理面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"},svccert:{CertType:"服务面",CertValidDate:"***",CertAlarm:"***",CrlStatus:"***"}}},mounted:function(){this.fetchData()},watch:{isQueryVersion:function(t,e){this.isQueryVersion&&this.isQueryHealth&&this.isQueryCert&&(this.version=this.tmpVersion)},isQueryHealth:function(t,e){this.isQueryVersion&&this.isQueryHealth&&this.isQueryCert&&("健康"===this.tmpHealthStatus?this.isAhealth=!0:this.isAhealth=!1)},isQueryCert:function(t,e){this.isQueryVersion&&this.isQueryHealth&&this.isQueryCert&&(this.tableData=this.tmpTableData,this.handleSpan())}},methods:{handleGetUserAmount:function(){var t=this;Object(h.d)({}).then(function(e){"00000000"===e.data.status?(t.useramount=e.data.data.total,t.isUhealth=!0):(t.useramount=0,t.isUhealth=!1)})},handleGetDataSize:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(c.b)("/datamanager/v1/size",t)})({}).then(function(e){"00000000"===e.data.status?(t.datasize=(e.data.data.size/1024/1024).toFixed(2),t.isDhealth=!0):(t.datasize=0,t.isDhealth=!1)})},queryVersion:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(c.b)("/AIVAULT/v1/version/",t)})().then(function(e){if("31000022"===e.data.status)var i=setTimeout(function(){t.queryVersion(),clearTimeout(i)},1e3);else t.tmpVersion=e.data.data.version.split("_")[0],t.isQueryVersion=!0}).finally(function(){var e=setTimeout(function(){t.queryHealth(),clearTimeout(e)},1e3)})},queryHealth:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(c.b)("/AIVAULT/v1/health",t)})().then(function(e){if("31000022"===e.data.status)var i=setTimeout(function(){t.queryHealth(),clearTimeout(i)},1e3);else t.tmpHealthStatus="ok"===e.data.msg?"健康":"不健康",t.isQueryHealth=!0}).finally(function(){var e=setTimeout(function(){t.queryCert(),clearTimeout(e)},1e3)})},queryCert:function(){var t=this;(function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(c.b)("/AIVAULT/v1/certStatus",t)})().then(function(e){if("31000022"===e.data.status)var i=setTimeout(function(){t.queryCert(),clearTimeout(i)},1e3);else t.tmpTableData=e.data.data,t.isQueryCert=!0})},fetchData:function(){this.handleGetUserAmount(),this.handleGetDataSize(),this.queryVersion()},handleSpan:function(){var t=this,e=this.tableData.filter(function(t){return"MGMT"===t.CertType}),i=this.tableData.filter(function(t){return"MGMT"!==t.CertType});this.tableData=e.concat(i),this.tableData.forEach(function(e,i){"MGMT"===e.CertType&&(t.mgmtcert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.mgmtcert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.mgmtcert.CertValidDate=e.CertValidDate),t.svccert.CertAlarm=""===e.CertAlarm?"正常":"不正常",t.svccert.CrlStatus="No CRL certificate has been imported."===e.CrlStatus?"未导入":"已导入",t.svccert.CertValidDate=e.CertValidDate})},handleBeforeUpload:function(t){this.isUploading=!0;var e=t.type.indexOf("zip")>-1,i=t.size/1024/1024<=50;return e||(this.$message.error(this.$t("ERR_UPLOAD_FILE_TYPE")),this.isUploading=!1),i||(this.$message.error(this.$t("ERR_UPLOAD_FILE_SIZE")),this.isUploading=!1),e&&i},handleDownload:function(){var t=this;return s()(n.a.mark(function e(){var i,r,a,s,o;return n.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t.isDownloading=!0,e.next=3,u();case 3:i=e.sent,r=new Blob([i.data],{type:"application/zip"}),a=i.headers["content-disposition"].split(";")[1].split("=")[1],window.navigator&&window.navigator.msSaveOrOpenBlob?(window.navigator.msSaveBlob(r,a),console.log(1)):(s=window.URL||window.webkitURL||window.moxURL,(o=document.createElement("a")).href=s.createObjectURL(r),o.download=a,document.body.appendChild(o),o.click(),document.body.removeChild(o),window.URL.revokeObjectURL(s)),t.isDownloading=!1;case 8:case"end":return e.stop()}},e,t)}))()},handleUploadSuccess:function(t,e,i){"00000000"===t.status?this.$message.success({message:this.$t("SUCCESS_UPLOAD")}):this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.isUploading=!1},handleUploadError:function(t,e,i){this.$message.warning({message:this.$t("ERR_UPLOAD")}),this.isUploading=!1}}},v={render:function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"home"},[r("div",{staticClass:"left"},[r("div",{staticClass:"left-box first-left"},[r("div",{staticClass:"left-name"},[t._v(t._s(t.$t("USER_AMOUNT")))]),t._v(" "),r("div",{staticClass:"left-num"},[t._v(t._s(t.useramount))])]),t._v(" "),r("div",{staticClass:"left-box"},[r("div",{staticClass:"left-name"},[t._v(t._s(t.$t("SYS_DATA_SIZE")))]),t._v(" "),r("div",{staticClass:"left-num"},[t._v(t._s(t.datasize))])])]),t._v(" "),r("div",{staticClass:"right"},[r("div",{staticClass:"right-box right-top"},[r("div",[r("div",{staticClass:"title"},[t._v(t._s(t.$t("TOOL_INFO")))])]),t._v(" "),r("div",{staticClass:"top-button"},[r("el-button",{staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-upload2",loading:t.isUploading},on:{click:function(e){t.isConfirmUploading=!0}}},[t._v(t._s(t.$t("BUTTON_UPLOAD")))]),t._v(" "),r("el-button",{staticStyle:{color:"#D3DCE9"},attrs:{type:"text",icon:"el-icon-download",loading:t.isDownloading},on:{click:t.handleDownload}},[t._v(t._s(t.$t("BUTTON_DOWNLOAD")))])],1),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("VERSION")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.version))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("HEALTH_STATUS")))]),t._v(" "),r("div",{staticClass:"health_info",staticStyle:{"margin-top":"5px"}},[r("div",{staticClass:"ai-vault-healthy",staticStyle:{display:"flex","flex-direction":"column","align-items":"center"}},[this.isAhealth?r("img",{staticStyle:{margin:"8px"},attrs:{src:i("nwfx")}}):r("img",{staticStyle:{margin:"8px"},attrs:{src:i("vigF")}}),t._v(" "),r("div",[t._v("Ai-Vault")])]),t._v(" "),r("div",{staticClass:"user-manager-healthy",staticStyle:{display:"flex","flex-direction":"column","align-items":"center"}},[this.isUhealth?r("img",{staticStyle:{margin:"8px"},attrs:{src:i("nwfx")}}):r("img",{staticStyle:{margin:"8px"},attrs:{src:i("vigF")}}),t._v(" "),r("div",[t._v("User-Manager")])]),t._v(" "),r("div",{staticClass:"data-manager-healthy",staticStyle:{display:"flex","flex-direction":"column","align-items":"center"}},[this.isDhealth?r("img",{staticStyle:{margin:"8px"},attrs:{src:i("nwfx")}}):r("img",{staticStyle:{margin:"8px"},attrs:{src:i("vigF")}}),t._v(" "),r("div",[t._v("Data-Manager")])])])])]),t._v(" "),r("div",{staticClass:"right-box"},[r("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertType))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertValidDate))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CertAlarm))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.mgmtcert.CrlStatus))])])]),t._v(" "),r("div",{staticClass:"right-box"},[r("div",{staticClass:"title"},[t._v(t._s(t.$t("CERT_INFO")))]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_TYPE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertType))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_VALID_DATE")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertValidDate))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CERT_ALARM")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CertAlarm))])]),t._v(" "),r("div",{staticClass:"info-block"},[r("div",{staticClass:"right_name"},[t._v(t._s(t.$t("COLUMN_CRL_STATUS")))]),t._v(" "),r("div",{staticClass:"right_info"},[t._v(t._s(t.svccert.CrlStatus))])])])]),t._v(" "),r("el-dialog",{attrs:{title:t.$t("UPLOAD_RISK"),visible:t.isConfirmUploading,width:"28%","close-on-click-modal":!1,modal:!1},on:{"update:visible":function(e){t.isConfirmUploading=e}}},[r("div",{staticClass:"dialog-tip"},[r("div",{staticStyle:{"margin-left":"16px","margin-right":"16px"}},[r("img",{attrs:{src:i("77VW")}})]),t._v("\n          "+t._s(t.$t("CONFIRM_UPLOAD_TIP"))+"\n        ")]),t._v(" "),r("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{staticClass:"dialog-button",on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BTN_CANCEL")))]),t._v(" "),r("el-upload",{staticClass:"upload-demo",staticStyle:{display:"inline-block"},attrs:{action:"/datamanager/v1/import","file-list":t.fileList,"before-upload":t.handleBeforeUpload,"show-file-list":!1,"on-success":t.handleUploadSuccess,"on-error":t.handleUploadError}},[r("el-button",{staticClass:"dialog-button",attrs:{type:"primary"},on:{click:function(e){t.isConfirmUploading=!1}}},[t._v(t._s(t.$t("BUTTON_UPLOAD")))])],1)],1)])],1)},staticRenderFns:[]};var d=i("VU/8")(f,v,!1,function(t){i("bRcy")},"data-v-22d0a2ca",null);e.default=d.exports},SldL:function(t,e){!function(e){"use strict";var i,r=Object.prototype,n=r.hasOwnProperty,a="function"==typeof Symbol?Symbol:{},s=a.iterator||"@@iterator",o=a.asyncIterator||"@@asyncIterator",l=a.toStringTag||"@@toStringTag",c="object"==typeof t,u=e.regeneratorRuntime;if(u)c&&(t.exports=u);else{(u=e.regeneratorRuntime=c?t.exports:{}).wrap=C;var h="suspendedStart",f="suspendedYield",v="executing",d="completed",_={},m={};m[s]=function(){return this};var p=Object.getPrototypeOf,g=p&&p(p(A([])));g&&g!==r&&n.call(g,s)&&(m=g);var y=x.prototype=w.prototype=Object.create(m);L.prototype=y.constructor=x,x.constructor=L,x[l]=L.displayName="GeneratorFunction",u.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===L||"GeneratorFunction"===(e.displayName||e.name))},u.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,x):(t.__proto__=x,l in t||(t[l]="GeneratorFunction")),t.prototype=Object.create(y),t},u.awrap=function(t){return{__await:t}},T(U.prototype),U.prototype[o]=function(){return this},u.AsyncIterator=U,u.async=function(t,e,i,r){var n=new U(C(t,e,i,r));return u.isGeneratorFunction(e)?n:n.next().then(function(t){return t.done?t.value:n.next()})},T(y),y[l]="Generator",y[s]=function(){return this},y.toString=function(){return"[object Generator]"},u.keys=function(t){var e=[];for(var i in t)e.push(i);return e.reverse(),function i(){for(;e.length;){var r=e.pop();if(r in t)return i.value=r,i.done=!1,i}return i.done=!0,i}},u.values=A,D.prototype={constructor:D,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=i,this.done=!1,this.delegate=null,this.method="next",this.arg=i,this.tryEntries.forEach(E),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=i)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(r,n){return o.type="throw",o.arg=t,e.next=r,n&&(e.method="next",e.arg=i),!!n}for(var a=this.tryEntries.length-1;a>=0;--a){var s=this.tryEntries[a],o=s.completion;if("root"===s.tryLoc)return r("end");if(s.tryLoc<=this.prev){var l=n.call(s,"catchLoc"),c=n.call(s,"finallyLoc");if(l&&c){if(this.prev<s.catchLoc)return r(s.catchLoc,!0);if(this.prev<s.finallyLoc)return r(s.finallyLoc)}else if(l){if(this.prev<s.catchLoc)return r(s.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<s.finallyLoc)return r(s.finallyLoc)}}}},abrupt:function(t,e){for(var i=this.tryEntries.length-1;i>=0;--i){var r=this.tryEntries[i];if(r.tryLoc<=this.prev&&n.call(r,"finallyLoc")&&this.prev<r.finallyLoc){var a=r;break}}a&&("break"===t||"continue"===t)&&a.tryLoc<=e&&e<=a.finallyLoc&&(a=null);var s=a?a.completion:{};return s.type=t,s.arg=e,a?(this.method="next",this.next=a.finallyLoc,_):this.complete(s)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),_},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var i=this.tryEntries[e];if(i.finallyLoc===t)return this.complete(i.completion,i.afterLoc),E(i),_}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var i=this.tryEntries[e];if(i.tryLoc===t){var r=i.completion;if("throw"===r.type){var n=r.arg;E(i)}return n}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:A(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=i),_}}}function C(t,e,i,r){var n=e&&e.prototype instanceof w?e:w,a=Object.create(n.prototype),s=new D(r||[]);return a._invoke=function(t,e,i){var r=h;return function(n,a){if(r===v)throw new Error("Generator is already running");if(r===d){if("throw"===n)throw a;return R()}for(i.method=n,i.arg=a;;){var s=i.delegate;if(s){var o=S(s,i);if(o){if(o===_)continue;return o}}if("next"===i.method)i.sent=i._sent=i.arg;else if("throw"===i.method){if(r===h)throw r=d,i.arg;i.dispatchException(i.arg)}else"return"===i.method&&i.abrupt("return",i.arg);r=v;var l=b(t,e,i);if("normal"===l.type){if(r=i.done?d:f,l.arg===_)continue;return{value:l.arg,done:i.done}}"throw"===l.type&&(r=d,i.method="throw",i.arg=l.arg)}}}(t,i,s),a}function b(t,e,i){try{return{type:"normal",arg:t.call(e,i)}}catch(t){return{type:"throw",arg:t}}}function w(){}function L(){}function x(){}function T(t){["next","throw","return"].forEach(function(e){t[e]=function(t){return this._invoke(e,t)}})}function U(t){var e;this._invoke=function(i,r){function a(){return new Promise(function(e,a){!function e(i,r,a,s){var o=b(t[i],t,r);if("throw"!==o.type){var l=o.arg,c=l.value;return c&&"object"==typeof c&&n.call(c,"__await")?Promise.resolve(c.__await).then(function(t){e("next",t,a,s)},function(t){e("throw",t,a,s)}):Promise.resolve(c).then(function(t){l.value=t,a(l)},s)}s(o.arg)}(i,r,e,a)})}return e=e?e.then(a,a):a()}}function S(t,e){var r=t.iterator[e.method];if(r===i){if(e.delegate=null,"throw"===e.method){if(t.iterator.return&&(e.method="return",e.arg=i,S(t,e),"throw"===e.method))return _;e.method="throw",e.arg=new TypeError("The iterator does not provide a 'throw' method")}return _}var n=b(r,t.iterator,e.arg);if("throw"===n.type)return e.method="throw",e.arg=n.arg,e.delegate=null,_;var a=n.arg;return a?a.done?(e[t.resultName]=a.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=i),e.delegate=null,_):a:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,_)}function O(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function E(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function D(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(O,this),this.reset(!0)}function A(t){if(t){var e=t[s];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,a=function e(){for(;++r<t.length;)if(n.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=i,e.done=!0,e};return a.next=a}}return{next:R}}function R(){return{value:i,done:!0}}}(function(){return this}()||Function("return this")())},Xxa5:function(t,e,i){t.exports=i("jyFz")},bRcy:function(t,e){},exGp:function(t,e,i){"use strict";e.__esModule=!0;var r,n=i("//Fk"),a=(r=n)&&r.__esModule?r:{default:r};e.default=function(t){return function(){var e=t.apply(this,arguments);return new a.default(function(t,i){return function r(n,s){try{var o=e[n](s),l=o.value}catch(t){return void i(t)}if(!o.done)return a.default.resolve(l).then(function(t){r("next",t)},function(t){r("throw",t)});t(l)}("next")})}}},jyFz:function(t,e,i){var r=function(){return this}()||Function("return this")(),n=r.regeneratorRuntime&&Object.getOwnPropertyNames(r).indexOf("regeneratorRuntime")>=0,a=n&&r.regeneratorRuntime;if(r.regeneratorRuntime=void 0,t.exports=i("SldL"),n)r.regeneratorRuntime=a;else try{delete r.regeneratorRuntime}catch(t){r.regeneratorRuntime=void 0}}});
//# sourceMappingURL=1.db87cdd339b055959ca2.js.map