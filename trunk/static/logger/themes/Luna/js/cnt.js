var _openstat=_openstat||[];(function(){var J="$Rev: 3964 $",o="openstat.net",i="openstat",b=_openstat,h="rating.openstat.ru",d="Openstat",C="openstat.net";function K(L){if(j(L)){return false}z(L);t(L);m(L);L.plugins.push({action:"plugin",fn:l});L.plugins.push({action:"plugin",fn:e});L.plugins.push({action:"plugin",fn:f});I(L);return true}function j(L){if(b.seen[L.counter]){return true}b.seen[L.counter]=true;return false}function z(O){var R=document;var S=navigator;var L=window;var N=screen;O._cookie=1;if(!R.cookie){R.cookie=i+"_test=1; path=/";O._cookie=R.cookie?1:0}if(parent!=L){try{O._referrer=parent.document.referrer||""}catch(Q){}}if(O._referrer||O._referrer==""){O._frame_referrer=R.referrer||""}else{O._referrer=R.referrer||""}O._location=L.location.href;O._title=R.title;O._o_location=O._i_location=O._location;O._o_referer=O._i_referer=O._referer;O._o_title=O._i_title=O._title;O._frame=(parent.frames&&parent.frames.length>0)?1:0;O._flash="";if(S.plugins&&S.plugins["Shockwave Flash"]){O._flash=S.plugins["Shockwave Flash"].description.split(" ")[2]}else{if(L.ActiveXObject){for(var M=10;M>=2;M--){try{var P=new ActiveXObject("ShockwaveFlash.ShockwaveFlash."+M);if(P){O._flash=M+".0";break}}catch(Q){}}}}if(N.colorDepth){O._color_depth=N.colorDepth}else{if(N.pixelDepth){O._color_depth=N.pixelDepth}}if(N.width&&N.height){O._screen=N.width+"x"+N.height}O._java_enabled=(S.javaEnabled()?"Y":"N");O._html5=c();O._part=D(O);O._protocol=R.location.protocol;O._url=((O._protocol=="https:")?"https://":"http://")+o;if(O.group){O._url+="/c/"+O.group}else{O._url+="/cnt"}O._url+="?cid="+O.counter}function c(){var M="",N,L;L=!!window.HTMLCanvasElement;M+=L?"1":"0";L=(navigator&&navigator.geolocation);M+=L?"1":"0";L=false;try{L=window.localStorage}catch(N){}M+=L?"1":"0";L=!!window.HTMLVideoElement;M+=L?"1":"0";L=!!window.HTMLAudioElement;M+=L?"1":"0";L=!!window.performance;M+=L?"1":"0";return M}function I(L){var M=L.queue=L.queue||[];M.opts=L;M.push=G;M.process=r;M.fn=H;M.push()}function m(L){var M=L.plugins=L.plugins||[];M.push=G;M.process=r;M.fn=function(N){return g(L,N)}}function H(M){var L=this.opts;if(L.plugins.length>0){return false}if(typeof(M)=="string"){M={url:M}}if(M.action=="data"){return y(L,M)}else{return q(L,M)}}function y(M,L){M._part=D(M,L);M.pagelevel=6;A(M,1);return true}function g(N,M){var O,P,L;if(M.fn){return M.fn(N,M)}L=M.plugin;O=b.plugins[L]=b.plugins[L]||{};if(O.loaded){return O.fn(N,M)}if(!O.loading){O.loading=true;P=M.src||"//"+o+"/plugins/"+L+".js";n(P)}return false}function q(N,M){var L;if(!M||!M.url){return true}if(M.url.charAt(0)=="/"){M.url=document.location.protocol+"//"+document.location.host+M.url}if(M.referrer&&M.referrer.charAt(0)=="/"){M.referrer=document.location.protocol+"//"+document.location.host+M.referrer}N._referrer=M.referrer||N._o_location;N._title=M.title||N._o_title;N._location=M.url;N._part=D(N,M);N._o_location=N._location;N._o_title=N._title;N.pagelevel=L;A(N,0);return true}function l(M){var L;M._location=M._i_location;M._referer=M._i_referer;M._title=M._i_title;M._part=D(M);M.pagelevel=L;A(M,0);return true}function D(O,N){var M,P,L;N=N||{};M=N.part||O.part;if(M){M=M.replace(/^\s+/,"").replace(/\s+$/,"")}if(O.vars){P={};for(L in O.vars){P[L]=O.vars[L]}}if(N.vars){P=P||{};for(L in N.vars){P[L]=N.vars[L]}}if(P&&M){P.part=M}if(P){return E(P)}return M}function v(M,L,N){var O=((typeof(M.pagelevel)!="undefined")?"&p="+M.pagelevel:"")+"&c="+M._cookie+"&fr="+M._frame+"&fl="+w(M._flash)+"&px="+M._color_depth+"&wh="+M._screen+"&j="+M._java_enabled+"&t="+(new Date()).getTimezoneOffset()+"&h5="+M._html5;if(!M.skip_url){O+="&pg="+w(k(M._location,2048/N))+"&r="+w(k(M._referrer,2048/N));if(M._frame_referrer){O+="&r1="+w(k(M._frame_referrer,2048/N))}if(!L&&N<2){O+="&title="+w(k(M._title))}}if(M._part){O+="&partname="+w(M._part)}return O}function A(O,M){var N,P,L;for(N=1;N<4;N++){P=v(O,M,N);if(P.length<1800){break}}L=new Image();L.src=O._url+P+"&rn="+Math.random();L.onload=function(){return}}function t(O){var M,L,N;if(typeof(O.image)=="undefined"&&typeof(O.image_url)=="undefined"){return}M=document.getElementById(i+O.counter);if(!M){if(typeof(O._onload_set)=="undefined"){O._onload_set=true;a(window,"load",function(){t(O)})}return}if(typeof(O.image_url)=="undefined"){if(O.image<1000){O.image_url="://"+C+"/i/"+O.image+".gif";if(O.color){O.image_url+="?tc="+O.color}}else{O.image_url="://"+C+"/digits?cid="+O.counter+"&ls=0&ln="+O.image;if(O.color){O.image_url+="&tc="+O.color}}}if(O.image_url.substring(0,1)==":"){O.image_url="http"+(("https:"==O._protocol)?"s":"")+O.image_url}L=document.createElement("a");L.target="_blank";L.href="http://"+h+"/site/"+O.counter;N=document.createElement("img");N.alt=d;N.border=0;N.src=O.image_url;L.appendChild(N);M.appendChild(L)}function e(L){if(L.track_links=="none"){L.track_links=null}if(L.track_links||L.track_class){a(window,"load",function(){F(L,L._url)})}return true}function F(N,L){var M=(navigator.appVersion.indexOf("MSIE")!=-1)?"click":"mousedown";a(document.body,M,function(O){if(!O){O=window.event}u(O,N,L)})}function u(R,P,N){var O;if(R.target){O=R.target}else{if(R.srcElement){O=R.srcElement}}if(O.nodeType==3){O=O.parentNode}var Q=O.tagName.toString().toLowerCase();while(O.parentNode&&O.parentNode.tagName&&((Q!="a"&&Q!="area")||!O.href)){O=O.parentNode;Q=O.tagName.toString().toLowerCase()}if(!O.href){return}if(P.track_class){var L=O.className.split("s");for(var M=0;M<L.length;M++){if(L[M]==P.track_class){P._referrer=document.location.href;P._location=O.href;P.pagelevel=3;A(P,1);return}}}if(!P.track_links||(P.track_links=="ext"&&window.location.hostname==O.hostname)){return}P._referrer=document.location.href;P._location=O.href;P.pagelevel=3;A(P,1)}function a(N,L,M){if(N.addEventListener){N.addEventListener(L,M,false)}else{if(N.attachEvent){N.attachEvent("on"+L,M)}}}function f(M){var L="";if(window.location.hostname=="loveplanet.ru"&&M.vars){if(M.vars.sex){L+="&sex="+w(M.vars.sex)}if(M.vars.age){L+="&age="+w(M.vars.age)}}s("openstat",M.counter,L);return true}function s(M,Q,N){var O="front.facetz.net";var P="//"+O+"/collect?source="+encodeURIComponent(M)+"&id="+encodeURIComponent(Q)+"&previous_url="+encodeURIComponent(document.referrer)+"&rn="+Math.random()+N;var L=new Image();L.src=P;L.onload=function(){return}}function k(M,L){if(!M){return M}if(!L){L=250}if(M.length>L){var N=M.indexOf("?");if(N!=-1){M=M.slice(0,N)}}if(M.length>L){M=M.substring(0,L)}return M}function w(O){if(typeof(encodeURIComponent)=="function"){return encodeURIComponent(O)}var P="";var M=O.length;for(var N=0;N<M;N++){var L=O.charCodeAt(N);if(L<128){P+=escape(O.charAt(N));continue}L=L.toString(16);P+="%u"+p(L.toUpperCase(),4,"0")}return P}function p(Q,L,P){var O=Q.length;if(O>=L){return Q}var N=L-O;for(var M=0;M<N;M++){Q=P+Q}return Q}function E(M){var L,O,P=[],N,R,Q={};switch(typeof(M)){case"number":case"boolean":case"null":return isFinite(M)?String(M):"null";case"string":O="";for(N=0;N<M.length;N++){R=M.charAt(N);if(R<" "||R==":"||R=="\\"){R=R.charCodeAt(0).toString(16);O+="\\x"+p(R,2,"0")}else{O+=R}}return O;case"object":if(!M){return"null"}for(L in M){if(M[L]!==Q[L]){O=E(M[L]);if(O){P[P.length]=E(L)+":"+O}}}return":"+P.join(":");default:return""}}function n(P){var O=document,N=document.location.protocol,L,M;L=O.createElement("script");L.async=true;L.type="text/javascript";L.src=("https:"==N?"https:":"http:")+P;M=O.getElementsByTagName("script")[0];M.parentNode.insertBefore(L,M)}function G(){var L;for(L=0;L<arguments.length;L++){this[this.length]=arguments[L]}this.process()}function r(){var M,L,N;for(M=0;M<this.length;M++){if(!this.fn(this[M])){break}}for(L=0;M<this.length;L++,M++){this[L]=this[M]}this.length=L;if(this.fnpost){this.fnpost()}}function x(){var L=b;if(L.plugins){return}L.plugins={};L.seen={};L.counters=[];L.push=G;L.process=r;L.fn=function(M){if(M.action=="plugin.loaded"){this.plugins[M.plugin].loaded=true;this.plugins[M.plugin].fn=M.fn}if(M.action=="counter"){if(K(M)){this.counters[this.counters.length]=M}}return true};L.fnpost=function(){var M,N;for(M=0;M<this.counters.length;M++){N=this.counters[M];N.plugins.push();N.queue.push()}return true};L.push()}function B(){var L=window[i];while(L){L.action="counter";b.push(L);L=L.next}window[i]=L}x();B()})();