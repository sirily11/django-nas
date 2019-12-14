(window["webpackJsonpelectron-react-template"]=window["webpackJsonpelectron-react-template"]||[]).push([[0],{516:function(e,t,a){e.exports=a(867)},521:function(e,t,a){},867:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),c=a(24),o=a.n(c),l=a(26),u=(a(521),a(153)),i=a(99),s=a(927),m=a(116);function d(){return r.a.createElement(s.a,{columns:2,divided:!0,style:{margin:10}},r.a.createElement(s.a.Row,null,r.a.createElement(s.a.Column,null,r.a.createElement("h1",null,"Raspberry NAS")),r.a.createElement(s.a.Column,{color:"blue"},r.a.createElement(m.a,{name:"database",size:"huge"}))))}a(324);var f=a(11),p=a.n(f),h=a(23),v=a(155),b=a(925),E=a(923),x=a(281),w=a(868),O=a(920),g=a(467),k=a(911),y=a(912),j=a(914),S=a(913),C=a(915),F=a(41),D=a(48),M=a(68),N=a(67),I=a(69),P=a(434),L=a(35),_=a.n(L),A="/system/",Y="/api/folder/",T="/api/download/";function z(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function U(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?z(a,!0).forEach((function(t){Object(P.a)(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):z(a).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}var q,H=function e(){var t=this;Object(F.a)(this,e),this.menus=void 0,this.currentFolder=void 0,this.errorMsg=void 0,this.getContent=function(){var e=Object(h.a)(p.a.mark((function e(a){var n,r,c;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,n=a?"".concat(Y).concat(a,"/"):Y,e.next=4,_.a.get(n);case 4:r=e.sent,c=r.data,t.menus=c.parents,t.currentFolder=c,t.errorMsg=void 0,e.next=15;break;case 11:e.prev=11,e.t0=e.catch(0),t.errorMsg=e.t0,t.currentFolder=void 0;case 15:case"end":return e.stop()}}),e,null,[[0,11]])})));return function(t){return e.apply(this,arguments)}}(),this.uploadFile=function(){var e=Object(h.a)(p.a.mark((function e(a,n){return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.delegateYield(p.a.mark((function e(){var r,c,o,l,u,i,s,m,d;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:r=0,c=!0,o=!1,l=void 0,e.prev=4,u=a[Symbol.iterator]();case 6:if(c=(i=u.next()).done){e.next=22;break}if(s=i.value,!t.currentFolder){e.next=18;break}return n(r,0),(m=new FormData).append("file",s),t.currentFolder.id&&m.append("parent",t.currentFolder.id.toString()),e.next=15,_.a.post("/api/file/",m,{headers:{"Content-Type":"multipart/form-data"},onUploadProgress:function(e){var t=Math.round(100*e.loaded/e.total);n(r,t)}});case 15:d=e.sent,t.currentFolder.files.push(d.data),t.currentFolder.total_size+=d.data.size;case 18:r+=1;case 19:c=!0,e.next=6;break;case 22:e.next=28;break;case 24:e.prev=24,e.t0=e.catch(4),o=!0,l=e.t0;case 28:e.prev=28,e.prev=29,c||null==u.return||u.return();case 31:if(e.prev=31,!o){e.next=34;break}throw l;case 34:return e.finish(31);case 35:return e.finish(28);case 36:n(r,100);case 37:case"end":return e.stop()}}),e,null,[[4,24,28,36],[29,,31,35]])}))(),"t0",2);case 2:e.next=7;break;case 4:e.prev=4,e.t1=e.catch(0),alert("Upload Failed: "+e.t1.toString());case 7:case"end":return e.stop()}}),e,null,[[0,4]])})));return function(t,a){return e.apply(this,arguments)}}(),this.deleteFile=function(){var e=Object(h.a)(p.a.mark((function e(a){return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,!window.confirm("Are you sure you want to delete this file?")||!t.currentFolder){e.next=8;break}return e.next=5,_.a.delete("".concat("/api/file/").concat(a,"/"));case 5:return e.sent,e.next=8,t.getContent(t.currentFolder.id);case 8:e.next=13;break;case 10:e.prev=10,e.t0=e.catch(0),alert("Upload Failed: "+e.t0.toString());case 13:case"end":return e.stop()}}),e,null,[[0,10]])})));return function(t){return e.apply(this,arguments)}}(),this.deleteFolder=function(){var e=Object(h.a)(p.a.mark((function e(a){return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.prev=0,!window.confirm("Are you sure you want to delete this folder?")||!t.currentFolder){e.next=8;break}return e.next=5,_.a.delete("".concat(Y).concat(a,"/"));case 5:return e.sent,e.next=8,t.getContent(t.currentFolder.id);case 8:e.next=13;break;case 10:e.prev=10,e.t0=e.catch(0),alert("Upload Failed: "+e.t0.toString());case 13:case"end":return e.stop()}}),e,null,[[0,10]])})));return function(t){return e.apply(this,arguments)}}(),this.createNewFolder=function(){var e=Object(h.a)(p.a.mark((function e(a){var n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.currentFolder){e.next=7;break}return e.next=3,_.a.post(Y,U({},a,{parent:t.currentFolder.id?t.currentFolder.id:null}));case 3:n=e.sent,t.currentFolder.folders.push(n.data),e.next=8;break;case 7:alert("Create new folder error: empty parent folder");case 8:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),this.renameFolder=function(){var e=Object(h.a)(p.a.mark((function e(a,n){var r,c;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.currentFolder){e.next=8;break}return e.next=3,_.a.patch("".concat(Y).concat(a,"/"),U({},n,{parent:t.currentFolder.id?t.currentFolder.id:null}));case 3:r=e.sent,(c=t.currentFolder.folders.findIndex((function(e){return e.id===a})))>-1&&(t.currentFolder.folders[c]=r.data),e.next=9;break;case 8:alert("Rename new folder error: empty parent folder");case 9:case"end":return e.stop()}}),e)})));return function(t,a){return e.apply(this,arguments)}}(),this.getDocument=function(){var e=Object(h.a)(p.a.mark((function e(t){var a;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,_.a.get("".concat("/api/document/").concat(t,"/"));case 2:return a=e.sent,e.abrupt("return",Promise.resolve(U({},a.data,{content:JSON.parse(a.data.content)})));case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),this.createNewDocument=function(){var e=Object(h.a)(p.a.mark((function e(a,n){var r;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,_.a.post("/api/document/",{name:a,parent:t.currentFolder&&t.currentFolder.id?t.currentFolder.id:null,content:JSON.stringify(n.ops)});case 2:r=e.sent,t.currentFolder&&t.currentFolder.documents.push(r.data);case 4:case"end":return e.stop()}}),e)})));return function(t,a){return e.apply(this,arguments)}}(),this.updateDocument=function(){var e=Object(h.a)(p.a.mark((function e(a,n,r){var c,o;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,_.a.patch("".concat("/api/document/").concat(a,"/"),{name:n,content:JSON.stringify(r.ops)});case 2:c=e.sent,t.currentFolder&&(o=t.currentFolder.documents.findIndex((function(e){return e.id===a})))>-1&&(t.currentFolder.documents[o]=c.data);case 4:case"end":return e.stop()}}),e)})));return function(t,a,n){return e.apply(this,arguments)}}(),this.deleteDocument=function(){var e=Object(h.a)(p.a.mark((function e(a){var n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.currentFolder){e.next=10;break}return console.log("delte document"),e.next=4,_.a.delete("".concat("/api/document/").concat(a,"/"));case 4:return n=e.sent,e.next=7,t.getContent(t.currentFolder.id);case 7:return e.abrupt("return",Promise.resolve(n.data));case 10:return alert("Create new folder error: empty parent folder"),e.abrupt("return",Promise.reject());case 12:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),this.menus=[]},B=function(e){function t(e){var a;return Object(F.a)(this,t),(a=Object(M.a)(this,Object(N.a)(t).call(this,e))).fetch=function(){var e=Object(h.a)(p.a.mark((function e(t){var n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a.setState({isLoading:!0}),n=a.state.nas,e.next=4,n.getContent(t);case 4:a.setState({nas:n,isLoading:!1});case 5:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),a.update=function(){a.setState({nas:a.state.nas})},a.state={nas:new H,update:a.update,isLoading:!1},a}return Object(I.a)(t,e),Object(D.a)(t,[{key:"componentDidUpdate",value:function(){var e=Object(h.a)(p.a.mark((function e(t){var a;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.props.match.params.id===t.match.params.id){e.next=4;break}return a=this.props.match.params.id,e.next=4,this.fetch(a);case 4:case"end":return e.stop()}}),e,this)})));return function(t){return e.apply(this,arguments)}}()},{key:"componentWillMount",value:function(){var e=Object(h.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t=this.props.match.params.id,e.next=3,this.fetch(t);case 3:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){return r.a.createElement(W.Provider,{value:this.state},this.props.children)}}]),t}(n.Component),R={nas:new H,update:function(){},isLoading:!1},W=r.a.createContext(R),J=a(204),G=a.n(J),V=a(205),K=a.n(V);a(606);!function(e){e.text="text",e.number="number",e.datetime="datetime",e.foreignkey="foreignkey",e.unknown="unknown",e.select="select",e.tomanyTable="tomany-table"}(q||(q={}));var $,Q,X=function(){function e(t){Object(F.a)(this,e),this.schemaList=void 0,t.forEach((function(e){e.extra&&e.extra.default&&(e.value=e.extra.default)})),this.schemaList=t}return Object(D.a)(e,[{key:"merge",value:function(e){this.schemaList=this.schemaList.map((function(t){if(e[t.name]){var a=e[t.name];if(t.widget==q.select){var n=t.extra&&t.extra.choices&&t.extra.choices.find((function(e){return e.value===a}));t.choice=n}else if(t.widget==q.foreignkey){var r=a;t.choice=r,t.value=a.value}else t.value=a}return t}))}},{key:"onSubmit",value:function(){console.log(this.schemaList);var e={};return this.schemaList.filter((function(e){return!e.readonly&&e.widget!==q.tomanyTable})).forEach((function(t){return e[t.name]=t.value})),console.log(e),e}}]),e}(),Z=function(){function e(t){Object(F.a)(this,e),this.schemaName=void 0,this.schemaName=t}return Object(D.a)(e,[{key:"merge",value:function(e,t){return[]}}]),e}();!function(e){e[e.image=0]="image",e[e.qrScan=1]="qrScan"}($||($={})),function(e){e[e.getInput=0]="getInput",e[e.getImage=1]="getImage"}(Q||(Q={}));var ee=function(e){function t(e,a,n){var r;return Object(F.a)(this,t),(r=Object(M.a)(this,Object(N.a)(t).call(this,n))).actionTypes=void 0,r.actionDone=void 0,r.schemaName=void 0,r.schemaName=n,r.actionTypes=e,r.actionDone=a,r}return Object(I.a)(t,e),Object(D.a)(t,null,[{key:"merge",value:function(e,t){return e.map((function(e){return t.forEach((function(t){t.schemaName==e.name&&(e.action=t)})),e}))}}]),t}(Z),te=function(e){function t(e,a){var n;return Object(F.a)(this,t),(n=Object(M.a)(this,Object(N.a)(t).call(this,a))).iconData=void 0,n.schemaName=void 0,n.iconData=e,n.schemaName=a,n}return Object(I.a)(t,e),Object(D.a)(t,null,[{key:"merge",value:function(e,t){return e.map((function(e){return t.forEach((function(t){t.schemaName==e.name&&(e.icon=t)})),e}))}}]),t}(Z),ae=a(908),ne=a(919),re=a(901);function ce(e){var t=e.schema,a=e.onSaved;return r.a.createElement("div",null,r.a.createElement(ne.a.Input,{"data-testid":"input-field",control:re.a,label:t.label,error:function(){if(t.required&&void 0===t.value)return{content:"This field is required",pointing:"below"}}(),onChange:function(e,t){var n=t.value;a(n)},defaultValue:t.value}),t.extra&&t.extra.help&&r.a.createElement(v.a,{color:"blue"},t.extra.help))}var oe=a(902);function le(e){var t=e.schema,a=e.onSaved;return r.a.createElement(ne.a.Select,{"data-testid":"select-field",control:oe.a,label:t.label,options:t.extra&&t.extra.choices?t.extra.choices.map((function(e){return{text:e.label,value:e.value,key:e.label}})):[],value:t.value,onChange:function(e,t){var n=t.value;return a(n)},placeholder:t.value?t.value:t.extra&&t.extra.default})}var ue=a(159),ie=a(928),se=a(906),me=a(907);function de(e){var t=e.schema,a=e.onSaved,c=e.url,o=Object(n.useState)(),u=Object(l.a)(o,2),i=u[0],m=u[1],d=Object(n.useState)(),f=Object(l.a)(d,2),b=f[0],E=f[1],x=Object(n.useState)(t.choice&&t.choice.value),O=Object(l.a)(x,2),g=O[0],k=O[1],y=Object(n.useState)(!1),j=Object(l.a)(y,2),S=j[0],C=j[1],F=Object(n.useState)(-1),D=Object(l.a)(F,2),M=D[0],N=D[1];function I(e){return"".concat(c,"/").concat(e)}var P=function(){var e=Object(h.a)(p.a.mark((function e(){var a,n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.extra){e.next=6;break}return a=I(t.extra.related_model&&t.extra.related_model.replace("-","_")+"/"),e.next=4,_.a.get(a);case 4:return n=e.sent,e.abrupt("return",n.data);case 6:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),L=function(){var e=Object(h.a)(p.a.mark((function e(){var a,n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!t.extra){e.next=6;break}return a=I(t.extra.related_model&&t.extra.related_model.replace("-","_")+"/"),e.next=4,_.a.request({method:"OPTIONS",url:a});case 4:n=e.sent,E(n.data.fields);case 6:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),A=function(){var e=Object(h.a)(p.a.mark((function e(a){var n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(C(!0),!t.extra){e.next=6;break}return n=I(t.extra.related_model&&t.extra.related_model.replace("-","_")+"/"+g+"/"),e.next=5,_.a.patch(n,a);case 5:e.sent;case 6:C(!1);case 7:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),Y=function(){var e=Object(h.a)(p.a.mark((function e(a){var n;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(C(!0),!t.extra){e.next=6;break}return n=I(t.extra.related_model&&t.extra.related_model.replace("-","_")+"/"),e.next=5,_.a.post(n,a);case 5:e.sent;case 6:C(!1);case 7:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}();return r.a.createElement(s.a,null,r.a.createElement(s.a.Row,{columns:"equal"},r.a.createElement(s.a.Column,{width:10},r.a.createElement(ue.a,{value:t.choice&&t.choice.value,labeled:!0,placeholder:"Select ".concat(t.label),fluid:!0,search:!0,selection:!0,onChange:function(t,n){var r=n.value;if(k(r),a(r),i){var c=i.find((function(e){return e.id===r}));e.select({label:c.name,value:c.id})}},options:void 0!==i?i.map((function(e){return{key:e.id,text:e.name,value:e.id}})):t.choice?[{text:t.choice.label,key:t.choice.value,value:t.choice.value}]:[],onClick:Object(h.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,P();case 2:(t=e.sent)&&m(t);case 4:case"end":return e.stop()}}),e)})))})),r.a.createElement(s.a.Column,null,r.a.createElement(w.a,{icon:"add",color:"blue",onClick:Object(h.a)(p.a.mark((function e(){return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return N(0),e.next=3,L();case 3:case"end":return e.stop()}}),e)})))}),r.a.createElement(w.a,{icon:"edit",color:"blue",disabled:void 0===t.value,onClick:Object(h.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return N(1),e.next=3,P();case 3:return t=e.sent,m(t),e.next=7,L();case 7:case"end":return e.stop()}}),e)})))}),r.a.createElement(ie.a,{open:0===M,onClose:function(){return N(-1)},fullWidth:!0},r.a.createElement(se.a,null,"Add ",t.label),r.a.createElement(me.a,null,b&&r.a.createElement(fe,{schemas:b,url:c,onSubmit:Y}))),r.a.createElement(ie.a,{open:1===M,onClose:function(){return N(-1)},fullWidth:!0},r.a.createElement(se.a,null,"Edit ",t.label),r.a.createElement(me.a,null,b&&r.a.createElement(fe,{schemas:b,values:i&&i.find((function(e){return e.id===g})),url:c,onSubmit:A,loading:S})))),t.required&&!t.value&&r.a.createElement(s.a.Column,null,r.a.createElement(v.a,{tag:!0,color:"red"},"Required"))))}var fe=function(e){function t(e){var a;return Object(F.a)(this,t),(a=Object(M.a)(this,Object(N.a)(t).call(this,e))).onSaved=function(e,t){var n=e;t.widget===q.number&&(n=parseInt(e)),t.value=n,a.setState({schemaList:a.state.schemaList})},a.state={schemaList:void 0,submitSuccess:void 0},a}return Object(I.a)(t,e),Object(D.a)(t,[{key:"componentDidMount",value:function(){var e=this.props,t=e.schemas,a=e.values,n=e.icons,r=e.actions,c=new X(t);if(a&&c.merge(a),n){var o=te.merge(c.schemaList,n);c.schemaList=o}if(r){var l=ee.merge(c.schemaList,r);c.schemaList=l}this.setState({schemaList:c})}},{key:"renderField",value:function(e){var t=this;switch(e.widget){case q.select:return r.a.createElement(le,{schema:e,onSaved:function(a){return t.onSaved(a,e)}});case q.foreignkey:return r.a.createElement(de,{select:function(a){e.choice=a,t.setState({schemaList:t.state.schemaList})},schema:e,onSaved:function(a){return t.onSaved(a,e)},url:this.props.url});case q.text:case q.number:return r.a.createElement(ce,{schema:e,onSaved:function(a){return t.onSaved(a,e)}});default:return r.a.createElement("div",{key:e.name})}}},{key:"render",value:function(){var e=this,t=this.state,a=t.schemaList,n=t.submitSuccess,c=this.props.loading;return r.a.createElement(ae.a,null,void 0!==n&&r.a.createElement(v.a,{basic:!0,color:n?"green":"red"},"Submitted ",n?"success":"failed"),r.a.createElement(ne.a,{loading:c},a&&a.schemaList.filter((function(e){return!e.readonly})).map((function(t){return r.a.createElement(ne.a.Field,{key:t.name},e.renderField(t))})),r.a.createElement(w.a,{loading:!0===c,onClick:Object(h.a)(p.a.mark((function t(){var n;return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!a||!e.props.onSubmit){t.next=12;break}return t.prev=1,n=a.onSubmit(),t.next=5,e.props.onSubmit(n);case 5:e.setState({submitSuccess:!0}),t.next=12;break;case 8:t.prev=8,t.t0=t.catch(1),alert(t.t0),e.setState({submitSuccess:!1});case 12:case"end":return t.stop()}}),t,null,[[1,8]])})))},"Submit")))}}]),t}(n.Component),pe=[{name:"name",label:"Folder Name",readonly:!1,required:!0,widget:q.text}];function he(e){var t=Object(n.useContext)(W),a=t.nas,c=t.update;return r.a.createElement(O.a,{open:e.open},r.a.createElement(O.a.Header,null,"Select files"),r.a.createElement(O.a.Content,null,r.a.createElement(fe,{schemas:pe,url:"",values:{name:e.selectedFolder.name},onSubmit:function(){var t=Object(h.a)(p.a.mark((function t(n){return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,a.renameFolder(e.selectedFolder.id,n);case 3:c(),setTimeout((function(){e.setOpen(!1)}),300),t.next=10;break;case 7:throw t.prev=7,t.t0=t.catch(0),t.t0;case 10:case"end":return t.stop()}}),t,null,[[0,7]])})));return function(e){return t.apply(this,arguments)}}()})),r.a.createElement(O.a.Actions,null,r.a.createElement(w.a,{basic:!0,color:"red",onClick:function(){return e.setOpen(!1)}},r.a.createElement(m.a,{name:"remove"})," No")))}var ve=a(918),be=(a(685),a(451)),Ee=a.n(be);function xe(e){var t=Object(n.useState)(),a=Object(l.a)(t,2),c=a[0],o=a[1],u=Object(n.useState)(),i=Object(l.a)(u,2),s=i[0],m=i[1],d=Object(n.useState)(!1),f=Object(l.a)(d,2),v=f[0],b=(f[1],e.document),E=Object(n.useContext)(W),x=E.nas,g=E.update;return void 0===s&&m(b?b.name:""),r.a.createElement(O.a,{open:e.open,centered:!1},r.a.createElement(O.a.Header,null,r.a.createElement(ve.a,{value:s,label:"You Document Title",onChange:function(e){m(e.target.value)},fullWidth:!0})),r.a.createElement(O.a.Content,null,r.a.createElement(Ee.a,{ref:function(e){return o(null!=e?e:void 0)},defaultValue:b&&b.content})),r.a.createElement(O.a.Actions,null,r.a.createElement(w.a,{onClick:function(){v?window.confirm("Are you sure you want to exit? You will lose unsave data.")&&e.setOpen(!1):e.setOpen(!1)}},"close"),r.a.createElement(w.a,{color:"blue",onClick:Object(h.a)(p.a.mark((function t(){var a;return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(t.prev=0,!c||!s){t.next=17;break}if(a=c.getEditor().getContents(),!b){t.next=8;break}return t.next=6,x.updateDocument(b.id,s,a);case 6:t.next=14;break;case 8:if(""===s){t.next=13;break}return t.next=11,x.createNewDocument(s,a);case 11:t.next=14;break;case 13:throw"Name should not be empty";case 14:g(),m(void 0),e.setOpen(!1);case 17:t.next=22;break;case 19:t.prev=19,t.t0=t.catch(0),alert(t.t0.toString());case 22:case"end":return t.stop()}}),t,null,[[0,19]])})))},"Save")))}var we=a(697).Player,Oe=[".jpg",".png",".bmp",".JPG",".gif"],ge=[".mov",".mp4",".avi",".m4v",".MOV"];function ke(){var e=Object(n.useContext)(W),t=e.nas,a=e.isLoading,c=e.update,o=Object(n.useState)(),u=Object(l.a)(o,2),i=u[0],s=u[1],d=Object(n.useState)(void 0),f=Object(l.a)(d,2),F=f[0],D=f[1],M=Object(n.useState)(void 0),N=Object(l.a)(M,2),I=N[0],P=N[1],L=Object(n.useState)(void 0),A=Object(l.a)(L,2),Y=A[0],z=A[1];function U(e){return Oe.includes(K.a.extname(e))}function q(e){return ge.includes(K.a.extname(e))}return r.a.createElement("div",null,r.a.createElement(v.a,{style:{zIndex:10,position:"absolute"}},"Total Size:"," ",t.currentFolder&&(t.currentFolder.total_size/1024/1024).toFixed(2)," ","MB"),r.a.createElement(b.a,{placeholder:!0,loading:a,style:{height:.7*window.innerHeight,overflow:"auto"}},r.a.createElement(k.a,{style:{height:"100%"}},t.errorMsg&&r.a.createElement(E.a,{error:!0},r.a.createElement(x.a,null,"Network Error"),r.a.createElement("div",null,t.errorMsg.toString())),t.currentFolder&&t.currentFolder.folders.map((function(e,a){return r.a.createElement(y.a,{button:!0,key:"folder-".concat(e.id),onClick:function(){window.location.href="#/home/".concat(e.id)}},r.a.createElement(S.a,null,r.a.createElement(m.a,{circular:!0,name:"folder",size:"large",color:"grey"})),r.a.createElement(j.a,{primary:e.name,secondary:G()(e.modified_at).format("MMM DD, YYYY")}),r.a.createElement(C.a,null,r.a.createElement(w.a.Group,null,r.a.createElement(w.a,{icon:!0,onClick:Object(h.a)(p.a.mark((function t(){var a,n;return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,_.a.post("".concat(T).concat(e.id));case 2:a=t.sent,(n=document.createElement("a")).href="".concat(a.data.download_url),console.log(n.href),document.body.appendChild(n),n.click(),document.body.removeChild(n);case 9:case"end":return t.stop()}}),t)})))},r.a.createElement(m.a,{name:"download"})),r.a.createElement(w.a,{icon:!0,color:"blue",edge:"end",onClick:Object(h.a)(p.a.mark((function t(){return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:z(e);case 1:case"end":return t.stop()}}),t)})))},r.a.createElement(m.a,{name:"edit"})),r.a.createElement(w.a,{icon:!0,edge:"end",onClick:Object(h.a)(p.a.mark((function a(){return p.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,t.deleteFolder(e.id);case 2:c();case 3:case"end":return a.stop()}}),a)})))},r.a.createElement(m.a,{name:"trash"})))))})),t.currentFolder&&t.currentFolder.documents.map((function(e,a){return r.a.createElement(y.a,{button:!0,key:"folder-".concat(e.id),onClick:Object(h.a)(p.a.mark((function a(){var n;return p.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,t.getDocument(e.id);case 2:n=a.sent,s(n);case 4:case"end":return a.stop()}}),a)})))},r.a.createElement(S.a,null,r.a.createElement(m.a,{circular:!0,name:"file pdf",size:"large",color:"red"})),r.a.createElement(j.a,{primary:e.name,secondary:G()(e.modified_at).format("MMM DD, YYYY")}),r.a.createElement(C.a,null,r.a.createElement(w.a.Group,null,r.a.createElement(w.a,{icon:!0,color:"blue",edge:"end",onClick:Object(h.a)(p.a.mark((function a(){var n;return p.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,t.getDocument(e.id);case 2:n=a.sent,s(n);case 4:case"end":return a.stop()}}),a)})))},r.a.createElement(m.a,{name:"edit"})),r.a.createElement(w.a,{icon:!0,edge:"end",onClick:Object(h.a)(p.a.mark((function a(){return p.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,t.deleteDocument(e.id);case 2:c();case 3:case"end":return a.stop()}}),a)})))},r.a.createElement(m.a,{name:"trash"})))))})),t.currentFolder&&t.currentFolder.files.map((function(e,a){return r.a.createElement(y.a,{button:!0,onClick:function(){U(e.file)?D(e.file):q(e.file)&&(console.log(e.file),e.transcode_filepath?P(e.transcode_filepath):alert("Playback is not avaliable"))},key:"file-".concat(e.id)},r.a.createElement(S.a,null,r.a.createElement(m.a,{name:(n=e.file,U(n)?"images":q(n)?"file video":"file"),circular:!0,size:"large",color:"teal"})),r.a.createElement(j.a,{primary:K.a.basename(e.filename),secondary:r.a.createElement(r.a.Fragment,null,r.a.createElement("label",null,G()(e.modified_at).format("MMM DD, YYYY")),r.a.createElement("p",null," ",(e.size/1024/1024).toFixed(2),"MB "))}),r.a.createElement(C.a,null,r.a.createElement(w.a.Group,null,r.a.createElement(w.a,{icon:!0,edge:"end",color:"blue","aria-label":"download",onClick:function(){var t=document.createElement("a");t.href="".concat(e.file),document.body.appendChild(t),t.click(),document.body.removeChild(t)}},r.a.createElement(m.a,{name:"download"})),r.a.createElement(w.a,{icon:!0,onClick:Object(h.a)(p.a.mark((function a(){return p.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,t.deleteFile(e.id);case 2:c();case 3:case"end":return a.stop()}}),a)})))},r.a.createElement(m.a,{name:"trash"})))));var n}))),Y&&r.a.createElement(he,{selectedFolder:Y,open:void 0!==Y,setOpen:function(e){!e&&z(void 0)}}),i&&r.a.createElement(xe,{open:void 0!==i,setOpen:function(e){!e&&s(void 0)},document:i}),r.a.createElement(O.a,{open:void 0!==F,onClose:function(){return D(void 0)}},r.a.createElement(g.a,{src:F,fluid:!0})),r.a.createElement(O.a,{open:void 0!==I,onClose:function(){return P(void 0)}},r.a.createElement(we,null,r.a.createElement("source",{src:I})))))}var ye=a(926),je=a(916);function Se(e){var t=Object(n.useContext)(W),a=t.nas,c=t.update,o=Object(n.useState)(),u=Object(l.a)(o,2),i=u[0],d=u[1],f=Object(n.useState)(),v=Object(l.a)(f,2),E=v[0],x=v[1];return r.a.createElement(O.a,{open:e.open},r.a.createElement(O.a.Header,null,"Select Files"),r.a.createElement(O.a.Content,null,r.a.createElement(s.a.Row,null,r.a.createElement("input",{type:"file",multiple:!0,name:"Upload file",onChange:function(e){var t=e.target.files;if(t){for(var a=[],n=0;n<t.length;n++)a.push(t[n]);d(a)}}})),E&&r.a.createElement(s.a.Row,{style:{marginTop:20}},r.a.createElement(b.a,null,r.a.createElement(je.a,{percent:E.progress,attached:"top",color:"green",active:!0}),E.currentName," ",E.currentIndex," /"," ",E.total,r.a.createElement(je.a,{percent:E.currentIndex/E.total*100,attached:"bottom",color:"blue",active:!0})))),r.a.createElement(O.a.Actions,null,r.a.createElement(w.a,{basic:!0,color:"red",onClick:function(){return e.setOpen(!1)}},r.a.createElement(m.a,{name:"remove"})," ",E?"Minimize":"Close"),r.a.createElement(w.a,{disabled:void 0===i,color:"green",loading:void 0!==E,inverted:!0,onClick:Object(h.a)(p.a.mark((function t(){return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(!i){t.next=5;break}return t.next=3,a.uploadFile(i,(function(e,t){x({total:i.length,currentIndex:e,currentName:i[e]?i[e].name:"Finished",progress:t})}));case 3:c(),setTimeout((function(){e.setOpen(!1),d(void 0),x(void 0)}),300);case 5:case"end":return t.stop()}}),t)})))},r.a.createElement(m.a,{name:"checkmark"})," Upload")))}var Ce=[{name:"name",label:"Folder Name",readonly:!1,required:!0,widget:q.text}];function Fe(e){var t=Object(n.useContext)(W),a=t.nas,c=t.update;return r.a.createElement(O.a,{open:e.open},r.a.createElement(O.a.Header,null,"New Folder"),r.a.createElement(O.a.Content,null,r.a.createElement(fe,{schemas:Ce,url:"",onSubmit:function(){var t=Object(h.a)(p.a.mark((function t(n){return p.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,a.createNewFolder(n);case 3:c(),setTimeout((function(){e.setOpen(!1)}),300),t.next=10;break;case 7:throw t.prev=7,t.t0=t.catch(0),t.t0;case 10:case"end":return t.stop()}}),t,null,[[0,7]])})));return function(e){return t.apply(this,arguments)}}()})),r.a.createElement(O.a.Actions,null,r.a.createElement(w.a,{basic:!0,color:"red",onClick:function(){return e.setOpen(!1)}},r.a.createElement(m.a,{name:"remove"})," No")))}function De(){var e=Object(n.useContext)(W).nas,t=Object(n.useState)(!1),a=Object(l.a)(t,2),c=a[0],o=a[1],i=Object(n.useState)(!1),d=Object(l.a)(i,2),f=d[0],p=d[1],h=Object(n.useState)(!1),v=Object(l.a)(h,2),b=v[0],E=v[1];return r.a.createElement(s.a,null,r.a.createElement(s.a.Column,{floated:"left",width:10,textAlign:"left"},r.a.createElement(ye.a,{size:"large"},r.a.createElement(ye.a.Section,null,r.a.createElement(u.b,{to:"/home"},"Root"),r.a.createElement(ye.a.Divider,{icon:"right chevron"})),e.menus.map((function(e){return r.a.createElement(ye.a.Section,{key:"menu-".concat(e.id)},r.a.createElement(u.b,{to:"/home/".concat(e.id)},e.name),r.a.createElement(ye.a.Divider,{icon:"right chevron"}))})))),r.a.createElement(s.a.Column,{floated:"right",width:6,textAlign:"right"},r.a.createElement(w.a.Group,null,r.a.createElement(w.a,{icon:!0,onClick:function(){return p(!0)}},r.a.createElement(m.a,{name:"folder"})),r.a.createElement(w.a,{icon:!0,color:"blue",onClick:function(){return o(!0)},disabled:void 0===e.currentFolder},r.a.createElement(m.a,{name:"upload"})),r.a.createElement(w.a,{icon:!0,color:"orange",onClick:function(){return E(!0)},disabled:void 0===e.currentFolder},r.a.createElement(m.a,{name:"edit"})))),r.a.createElement(Se,{open:c,setOpen:o}),r.a.createElement(Fe,{open:f,setOpen:p}),r.a.createElement(xe,{open:b,setOpen:E}))}var Me=function(e){function t(e){var a;return Object(F.a)(this,t),(a=Object(M.a)(this,Object(N.a)(t).call(this,e))).fetchSystemInfo=Object(h.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,_.a.get(A);case 2:return t=e.sent,e.abrupt("return",Promise.resolve(t.data));case 4:case"end":return e.stop()}}),e)}))),a.state={},a}return Object(I.a)(t,e),Object(D.a)(t,[{key:"componentDidMount",value:function(){var e=Object(h.a)(p.a.mark((function e(){var t;return p.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.fetchSystemInfo();case 2:(t=e.sent)&&this.setState({systemInfo:t});case 4:case"end":return e.stop()}}),e,this)})));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){return r.a.createElement(Ne.Provider,{value:this.state},this.props.children)}}]),t}(n.Component),Ne=r.a.createContext({});function Ie(){var e=Object(n.useContext)(Ne).systemInfo;return void 0===e?r.a.createElement(E.a,null,r.a.createElement("p",null,"No Info Avaliable currently")):r.a.createElement("div",null,r.a.createElement("span",null,"Used Sapce: ",(e.disk.used/1024/1024).toFixed(2),"MB/",(e.disk.total/1024/1024).toFixed(2),"MB"),r.a.createElement(je.a,{percent:(e.disk.used/e.disk.total*100).toFixed(2),progress:!0,color:"green"}))}function Pe(){return r.a.createElement("div",{id:"home"},r.a.createElement(ae.a,null,r.a.createElement(d,null),r.a.createElement(b.a,null,r.a.createElement(De,null),r.a.createElement(ke,null),r.a.createElement(Ie,null))))}var Le=a(117);function _e(e){var t=e.title,a=e.used,n=e.total,c=e.color,o=e.color2,l=[{name:"Used",value:a},{name:"Available",value:n-a}];return r.a.createElement(b.a,null,r.a.createElement(Le.d,{minHeight:300,height:"100%",width:"100%",minWidth:200},r.a.createElement(Le.c,null,r.a.createElement(Le.b,{data:l,dataKey:"value",label:!0,fill:c,isAnimationActive:!1},r.a.createElement(Le.a,{fill:c}),r.a.createElement(Le.a,{fill:o})),r.a.createElement(Le.e,null))),r.a.createElement("span",null,t))}function Ae(){var e=Object(n.useContext)(Ne).systemInfo;return void 0===e?r.a.createElement("div",null,"Infomation Not Available"):r.a.createElement("div",{id:"home",style:{width:"100%",color:"black"}},r.a.createElement(ae.a,null,r.a.createElement("h1",null,"System Info"),r.a.createElement(s.a,{columns:2},r.a.createElement(s.a.Column,null,r.a.createElement(_e,{used:Math.round(e.disk.used/1024/1024),total:Math.round(e.disk.total/1024/1024),title:"Disk(MB)",color:"#0088FE",color2:"orange"})),r.a.createElement(s.a.Column,null,r.a.createElement(_e,{used:Math.round(e.memory.used/1024/1024),total:Math.round(e.memory.total/1024/1024),title:"Memory(MB)",color:"#0088FE",color2:"orange"})),r.a.createElement(s.a.Column,null,r.a.createElement(_e,{used:e.cpu,total:100,title:"CPU Usage(Percentage)",color:"#0088FE",color2:"orange"})),r.a.createElement(s.a.Column,null,r.a.createElement(b.a,{style:{height:"100%"}},r.a.createElement("h4",null,"Temperature"),r.a.createElement("h1",null,e.temperature?e.temperature.toFixed(1):"None"))),r.a.createElement(s.a.Column,null,r.a.createElement(b.a,{style:{height:"100%"}},r.a.createElement("h4",null,"Humidity"),r.a.createElement("h1",null,e.humidity?e.humidity.toFixed(1):"None"))),r.a.createElement(s.a.Column,null,r.a.createElement(b.a,{style:{height:"100%"}},r.a.createElement("h4",null,"Pressure"),r.a.createElement("h1",null,e.pressure?e.pressure.toFixed(2):"None"))))))}var Ye=a(929),Te=a(924),ze=a(465),Ue=a.n(ze),qe=a(917);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var He=a(466);o.a.render(r.a.createElement(He.I18nProvider,{catalogs:{}},r.a.createElement((function(){var e=Object(n.useState)(!1),t=Object(l.a)(e,2),a=t[0],c=t[1],o=Object(n.useState)(!1),s=Object(l.a)(o,2),d=s[0],f=s[1];return r.a.createElement(Me,null,r.a.createElement(u.a,null,r.a.createElement(Ye.a.Pushable,{style:{margin:0}},r.a.createElement(Ye.a,{style:{boxShadow:"none",border:"none"},as:Te.a,animation:"push",icon:"labeled",onHide:function(){return c(!1)},vertical:!0,visible:a,width:"thin"},r.a.createElement(Te.a.Item,{as:"a",href:"#/home"},r.a.createElement(m.a,{name:"home"}),"Home"),r.a.createElement(Te.a.Item,{as:"a",href:"#/info"},r.a.createElement(m.a,{name:"info"}),"System Info")),r.a.createElement(Ye.a.Pusher,null,d&&r.a.createElement(qe.a,{onClick:function(){return c(!a)},style:{position:"absolute"}},r.a.createElement(Ue.a,null)),r.a.createElement("div",{style:{height:"100%"}},r.a.createElement(i.b,{exact:!0,path:"/",component:function(){return r.a.createElement(i.a,{to:"/home"})}}),r.a.createElement(i.b,{exact:!0,path:"/home/:id?",component:function(e){return f(!0),r.a.createElement(B,e,r.a.createElement(Pe,null))}}),r.a.createElement(i.b,{exact:!0,path:"/info",component:function(e){return f(!0),r.a.createElement(Ae,null)}}))))))}),null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[516,1,2]]]);
//# sourceMappingURL=main.b6621004.chunk.js.map