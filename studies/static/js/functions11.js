// before uploading this file, remember to change _local to false
// this is so that it calls the database query page on www.w3.org rather than on people
// this is for version 8+ pickers

var _view = 'alphabet';
var _views = new Array;
var _hints = new Array;
var _phonicstr = ''; // captures phonemes associated with character selections in phonic view
var _n11n = 'nfc';
var _local = false;
var _refocus = true;

function closewindow() {
    if (window.opener && window.opener.copyoutput) {
        window.opener.copyoutput(document.getElementById('output').value);
		}
	}


function addandcapture (ch, node) { 
	while (node.previousSibling && (! node.className.match(/ph/))) {
		node = node.previousSibling;
		}
	if (node.alt) {
		document.getElementById('phondata').value += node.alt;
		}
	add(ch); if( node.parentNode.className.match(/sound/) ) { node.parentNode.style.display = "none"; }
	}

function oldaddandcapture (ch, node) { 
	if (_view == 'phonic' || _view == 'phonic2') { 
		while (node.previousSibling && (! node.className.match(/ph/))) {
			node = node.previousSibling;
			}
		}
	if (node.alt) {
		_phonicstr += node.alt;
		}
	add(ch); if( node.parentNode.className.match(/sound/) ) { node.parentNode.style.display = "none"; }
	}

function add(ch) { 
	// ch: string, the text to be added
	// _cluster: boolean, global variable, set if this is a consonant cluster (used for vowels that surround base)
	// _view: string, indicates which view is showing - this is important, since non-intelligent ordering is needed in the default view
	
	if (document.getElementById('output').style.display == 'none') { return; }
	var outputNode = document.getElementById( 'output' ); // points to the output textarea

	
	//IE support
	if (document.selection) { 
		outputNode.focus();
	    range = document.selection.createRange();
		
		range.text = ch; 
	    range.select(); 
		if (_refocus) { outputNode.focus(); }
		}
	// Mozilla and Safari support
	else if (outputNode.selectionStart || outputNode.selectionStart == '0') {
		var startPos = outputNode.selectionStart;
		var endPos = outputNode.selectionEnd;
		var cursorPos = startPos;
		var scrollTop = outputNode.scrollTop;
		var baselength = 0;
		
		outputNode.value = outputNode.value.substring(0, startPos)
              + ch
              + outputNode.value.substring(endPos, outputNode.value.length);
		cursorPos += ch.length;

		if (_refocus) { outputNode.focus(); }
		outputNode.selectionStart = cursorPos;
		outputNode.selectionEnd = cursorPos;
		//outputNode.scrollTop = scrollTop;
		}
	else {
		outputNode.value += ch;
		if (_refocus) { outputNode.focus(); }
		}
		
	// normalize
	if (_n11n=='nfc') { outputNode.value = nfc(outputNode.value); }
	else if (_n11n=='nfd') { outputNode.value = nfd(outputNode.value);}
	//var pairs = outputNode.value.match(/[\u0EC8\u0EC9\u0ECA\u0ECB][\u0E31\u0ECD\u0EC7\u0ECC\u0ECE\u0E38\u0E39\u0E3C\u0E35\u0E36\u0E37\u0E3A]/g);
	//if (pairs != null) {
		//for (var i=0; i<pairs.length; i++) { 
			//outputNode.value = outputNode.value.replace(pairs[i], pairs[i].charAt(1)+pairs[i].charAt(0));
			//}
		//}

	}

	

	
	
function deleteAll () {
	var outputNode = document.getElementById( 'output' );
	outputNode.value = "";
	}

function selectFont ( newFont ) {
	document.getElementById( 'output' ).style.fontFamily = newFont;
	document.getElementById('fontgrid').style.fontFamily = newFont;
	//for (i=0; i<_views.length; i++) {
		//document.getElementById(_views[i]).style.fontFamily = newFont;
		//}
	document.getElementById('fontName').value="";
	}
	
function customFont ( newFont ) { 
	document.getElementById( 'output' ).style.fontFamily = newFont;
	document.getElementById('fontgrid').style.fontFamily = newFont;
	//for (i=0; i<_views.length; i++) {
		//document.getElementById(_views[i]).style.fontFamily = newFont;
		//}
	document.getElementById('fontList').value='0';
	}
	
function changeFontSize ( newSize ) {
	document.getElementById( 'output' ).style.fontSize = newSize + 'px';
	document.getElementById('fontgrid').style.fontSize = newSize + 'px';
	}
	

function searchFor ( str, scriptname ) { 
	// set  border width according to current view
//	var borderwidth = '1px';
//	if (_view == 'shape') { borderwidth = '2px' } 

	var str = str.replace( /\:/g, '\\b' );
	var re = new RegExp(str, "i"); 
	var characters = new Array; 
//	for (view=0; view<_views.length; view++) {
//		if (document.getElementById(_views[view]).style.display != 'none') {
//			characters = document.getElementById(_views[view]).getElementsByTagName( 'img' );
//			}
//		}
// this if for current view only	characters = document.getElementById(_view).getElementsByTagName( 'img' );
	
	for (view=0; view<_views.length; view++) {
		borderwidth = '1px';
		//if (_views[view] == 'shape') { borderwidth = '2px' } 
		characters = document.getElementById(_views[view]).getElementsByTagName( 'img' );
		for (var i = 0; i < characters.length; i++ ) {
			if (! characters[i].className.match(/ph/)) {
				characters[i].style.border = '0';
				titletext = characters[i].title.toLowerCase();
				titletext = titletext.replace(scriptname, '');
				if (titletext.search(re, 0) > -1 ) {
					characters[i].style.border = borderwidth+' solid red';
					}
				}
			}
		characters = document.getElementById('shape').getElementsByTagName( 'span' );
		for (var i = 0; i < characters.length; i++ ) {
			if (! characters[i].className.match(/ph/)) {
				characters[i].style.border = '0';
				titletext = characters[i].title.toLowerCase();
				titletext = titletext.replace(scriptname, '');
				if (titletext.search(re, 0) > -1 ) {
					characters[i].style.border = borderwidth+' solid red';
					}
				}
			}
		}
	}
	


function convertCP2Char ( textString ) { 
  var outputString = '';
  textString = textString.replace(/[^a-fA-F0-9]/g, ' ');
  textString = textString.replace(/^\s+/, '');
  textString = textString.replace(/\s+$/, '');
  if (textString.length == 0) { return ""; }
        textString = textString.replace(/\s+/g, ' ');
  var listArray = textString.split(' ');
  for ( var i = 0; i < listArray.length; i++ ) {
    var n = parseInt(listArray[i], 16);
    if (n <= 0xFFFF) {
		outputString += String.fromCharCode(n);
		} 
	else if (n <= 0x10FFFF) {
		n -= 0x10000
		outputString += String.fromCharCode(0xD800 | (n >> 10)) + String.fromCharCode(0xDC00 | (n & 0x3FF));
		} 
	else {
		outputString += 'convertCP2Char error: Code point out of range: '+textString;
		}
	}
  return( outputString );
  }
	
	
	
function changeHighlight ( key ) {
	if (key == 'none' || key == 'off' || key == 'Off' ) { _highlightOn = false; }
	if (key == 'shape' ) { _highlightOn = 'true'; }
	}
	
	
function hblank () {
	// remove character information
	span = document.createElement( 'span' );
	span.setAttribute( 'id', 'charname' );
	span.appendChild(document.createTextNode( '\u00A0' ));
	var chardata = document.getElementById('chardata');	
	chardata.replaceChild( span, chardata.firstChild );
	}


function h ( node ) {
	// display character information
	span = document.createElement( 'span' );
	span.setAttribute( 'id', 'charname' );
	charinfo = document.createTextNode( node.title );
	span.appendChild(charinfo);
	var chardata = document.getElementById('chardata');	
	chardata.replaceChild( span, chardata.firstChild );
	}



function u ( node ) {
	}

	

	
	
function switchView (toView) {
	// toView: string, id of the div surrounding the content to be viewed
	// _view: string, stores the name of the div id so that addchar() can act in a view sensitive way
	
	_view = toView;
	
	var views = document.getElementById('tables').childNodes;
	for (var i=0; i<views.length; i++) {
		if (views[i].nodeName == 'DIV') { views[i].style.display = 'none'; }
		}

	//var viewselection = document.getElementById('views');
	//var buttons = viewselection.getElementsByTagName('BUTTON');
	//for (var i=0; i<buttons.length; i++) {
	//	buttons[i].className = 'off';
	//	}
		
	document.getElementById(toView).style.display = 'block';
	// document.getElementById('show'+toView).className = 'on';
	}
	

function switchNotes (toView) {
	// toView: string, id of the div surrounding the content to be viewed
	
	
	var views = document.getElementById('notes').childNodes;
	for (var i=0; i<views.length; i++) {
		if (views[i].nodeName == 'DIV') { views[i].style.display = 'none'; }
		}

	var viewselection = document.getElementById('views');
	var buttons = viewselection.getElementsByTagName('BUTTON');
	for (var i=0; i<buttons.length; i++) {
		buttons[i].className = 'off';
		}
		
	document.getElementById(toView).style.display = 'block';
	document.getElementById('show'+toView).className = 'on';
	}


function hideOutput () {
	document.getElementById('output').style.height = '0px'; 
	document.getElementById('restoreOutput').style.display = 'block';
	document.getElementById('buttons').style.display = 'none';
	}
	
function unhideOutput () {
	if (document.getElementById('output').style.display == 'none') {
		//document.getElementById('output').style.height = (document.getElementById('rows').value*100)+'px';
		document.getElementById('output').style.display = 'block';
		document.getElementById('buttons').style.display = 'block';
		document.getElementById('showOutput').replaceChild(document.createTextNode('Disable output'), document.getElementById('showOutput').firstChild);
		}
	else {
		document.getElementById('output').style.display = 'none';
		document.getElementById('buttons').style.display = 'none';
		document.getElementById('showOutput').replaceChild(document.createTextNode('Enable output'), document.getElementById('showOutput').firstChild);
		}
	}


function transcribe (node, direction) { 
	var chstring=''; // the text to be converted
	
	// get the highlighted text, or default to all text
	//IE support
	if (document.selection) { 
		//outputNode.focus();
	    chstring = document.selection.createRange().text;
		}
	// Mozilla and Safari support
	else if (node.selectionStart || node.selectionStart == '0') {
		chstring = node.value.substring(node.selectionStart, node.selectionEnd);
		}

	// add a space to avoid breaking on lookahead; if no selection, try whole field; if still nothing, abort
	chstring = chstring.toLowerCase()+' ';

	if (chstring==' ') { chstring = node.value.toLowerCase()+' '; }
	if (chstring==' ') { return; }

	output = dotranscription(chstring, direction);
	
	node.value = node.value+output;
	node.focus();
	}

	
function createshapelist (node) {
	var chstring = node.value;
	codepoints = window.open('http://people.w3.org/rishida/scripts/pickers/createshapelist.php?characters='+chstring, 'codepoints'); codepoints.focus();
	}

function showcodepoints (node) {
	var list = node.value;
	if (list=='') { return; }
	
	codepoints = window.open('http://people.w3.org/rishida/tools/analysestring?list='+encodeURIComponent(list)+'&smallgraphics=on&noblock=on&nonotes=on&compact=on&nounicode', 'codepoints'); codepoints.focus();
	}
	
	
function showdetail (node) {
	var list = node.value;
	if (list=='') { return; }
	
	//if (! _local) {
	//detail = window.open('http://www.w3.org/People/Ishida/php/showchars/index.php?codepoints='+encodeURIComponent(list), 'detail'); detail.focus();
	//	}
	//else { 
		detail = window.open('http://people.w3.org/rishida/tools/analysestring?list='+encodeURIComponent(list), 'detail'); detail.focus();
	//	}
	}
	
	
	
function closeCodepoints () {
	document.getElementById('codepoints').style.display = 'none';
	document.getElementById('shape').style.display = 'block';
	document.getElementById('chardata').style.display = 'block';
	document.getElementById('buttons').style.display = 'block';
	document.getElementById('latin').style.display = 'block';
	}

	

// INITIALISATION
function setReveal ( node ) {
	node.onmouseover = function(){ revealphones(node) };
	node.onclick = function () { addfromtranscript(node) };
	}
	
function setMouseover ( node ) {
	node.onmouseover = function(){ h(node) };
	}
	
function setBlankMouseover ( node ) {
	node.onmouseover = function(){ hblank() };
	}
	
function setMouseout ( node ) {
	node.onmouseout = function(){ u(node) };
	}
	
	
function setOnclick ( node, ch ) {
	node.onclick = function(){ add(ch) };
	}
	
function event_mouseoverChar ()  {
	// display character information
	span = document.createElement( 'span' );
	span.setAttribute( 'id', 'charname' );
	charinfo = document.createTextNode( this.title );
	span.appendChild(charinfo);
	var chardata = document.getElementById('chardata');	
	chardata.replaceChild( span, chardata.firstChild );
	}
	
function event_clickOnChar () {
	add(this.alt);
	}
function event_clickOnTranscriptionChar () {
	add(this.firstChild.data);
	}
function event_clickOnSpanChar () {
	add(this.firstChild.nodeValue);
	}
function event_clickOnPhone () {
	addandcapture(this.alt, this);
	}
function event_mouseoverPhone () {
	revealphones(this);
	}
function event_clickOnPhoneLabel () {
	addfromtranscript(this);
	}
	
function setOnclickPhone ( node, ch ) {
	node.onclick = function(){ addandcapture(ch, node) };
	}
	
function titleSort (a, b) {
	return parseInt(a.title, 16)-parseInt(b.title, 16);
	}

	
function initialise() { 
	// _views: array, listing ids of all view divs
	
	document.getElementById('output').contentEditable = 'true';
	
	// set up a list of all views in global _views variable
	var viewnodes = document.getElementById('tables').childNodes;
	var count = 0;
	for (i=0; i<viewnodes.length; i++) {
		if (viewnodes[i].nodeName == 'DIV' || viewnodes[i].nodeName == 'div') { _views[count] = viewnodes[i].id; count++; }
		}
		
	// stop IE changing the focus when clicking on an img
	//if (document.all && document.getElementById('alphabet')) {  
	//	document.getElementById('alphabet').onselectstart = function () { return false };
	//	}


	//  SET MOUSEOVERS
	// set mouseover/mouseout functions for all imgs in all views except class:ph and class:noMouseover
	for (i=0; i<_views.length; i++) {
		var characters = document.getElementById(_views[i]).getElementsByTagName( 'img' ); 
		for (var j = 0; j < characters.length; j++ ) {
			if ((! characters[j].className.match(/ph/)) && (! characters[j].className.match(/noMouseover/)) && (! characters[j].className.match(/lite/))) { 
				characters[j].onmouseover = event_mouseoverChar;
				}
			else if (characters[j].className.match(/ph/)) {
				
				}
			else if (characters[j].className.match(/lite/)) {
				
				}
			else {
				setBlankMouseover(characters[j]);
				}
			}
		}

	// SET ONCLICKS
	for (i=0; i<_views.length; i++) {
		var currentview = document.getElementById(_views[i]);
		var characters = document.getElementById(_views[i]).getElementsByTagName( 'img' ); 
		if (currentview.className == 'phonic') {
			for (var n = 0; n < characters.length; n++ ) {
				if(! characters[n].className.match(/noOnclick/)) { 
					characters[n].onclick = event_clickOnPhone;
					}
				}
			}
		else { 
			for (var n = 0; n < characters.length; n++ ) {
				if(! characters[n].className.match(/noOnclick/)) { 
					characters[n].onclick = event_clickOnChar;
					}
				}
			}
		}
		
	
	// set onlclicks for transcription characters	
	if (document.getElementById('phonemelist')) {
	var transcriptnodes = document.getElementById('phonemelist').childNodes; 
	for (var n = 0; n < transcriptnodes.length; n++ ) {
		if(transcriptnodes[n].nodeName == 'SPAN' || viewnodes[i].nodeName == 'span') { 
			transcriptnodes[n].onclick = event_clickOnTranscriptionChar; 
			}
		} 
	}



	// set up font grid
	if (document.getElementById('fontgrid')) {
		var container = document.getElementById('fontgrid');
		var characters = new Array;
		var count = 0;
		var charNodes = document.getElementById('alphabet').getElementsByTagName( 'img' );
		for (i=0; i<charNodes.length; i++) {
			if (! charNodes[i].className.match(/nogrid/)) {
				characters[count] = { title: charNodes[i].title, alt: charNodes[i].alt }; 
				count++;
				}
			}
		characters.sort(titleSort); 
		
		for (j=0; j<characters.length; j++) {
			var span = document.createElement('span');
			var text = document.createTextNode(characters[j].alt);
			span.title = characters[j].title;
			span.appendChild(text);
			span.onmouseover = event_mouseoverChar;
			span.onclick = event_clickOnSpanChar;
			container.appendChild(span);
			container.appendChild(document.createTextNode(' '));
			}
		// set the font from what's currently indicated in the font selection boxes
		customfont = document.getElementById('fontName').value; 
		listfont = document.getElementById('fontList').value; 
		if (customfont) { container.style.fontFamily = customfont; }
		else { container.style.fontFamily = listfont; }
		//container.appendChild(closeSA);
		//if (document.all) {  // stop IE changing the focus when clicking on an img
		//	for (i=0; i<_views.length; i++) {
		//		document.getElementById(_views[i]).onselectstart = function () { return false };
		//		}
		//	}
		document.getElementById('output').focus();
		}
	
	
	// SET REVEAL MOUSEOVER ON IMAGES IN PHONIC
	for (n=0; n<_views.length; n++) { 
		if (document.getElementById(_views[n]).className == 'phonic') { 
			var phonedivs = document.getElementById(_views[n]).getElementsByTagName('DIV');
			// remove all spaces
			for (i=0; i<phonedivs.length; i++) {
				if (phonedivs[i].className == 'soundselector') {
					var soundselector = phonedivs[i];
					imgs = phonedivs[i].childNodes;
					for (j=0; j<imgs.length; j++) {
						if (imgs[j].nodeType == 3) {
							soundselector.removeChild(imgs[j]);
							}
						}
					}
				}
			for (i=0; i<phonedivs.length; i++) {
				if (phonedivs[i].className == 'soundselector') {
					//var soundselector = phonedivs[i];
					imgs = phonedivs[i].childNodes;
					for (j=0; j<imgs.length; j++) {
						if (imgs[j].nodeName == 'IMG') {
							imgs[j].onclick = event_clickOnPhoneLabel;
							imgs[j].onmouseover = event_mouseoverPhone;
							//setReveal(imgs[j]);
							imgs[j].nextSibling.style.display = 'none';
							}
						}
					}
				}
			}
		}
	}

//window.onload = function() { initialise(); localInitialise(); };
var _highlightOn = true;


function showallphones () {
	var phoneversion = 'phonic';
		var phonedivs = document.getElementById(phoneversion).getElementsByTagName('DIV');
		for (i=0; i<phonedivs.length; i++) {
			if (phonedivs[i].className == 'soundselector') {
				var soundselector = phonedivs[i];
				imgs = phonedivs[i].childNodes;
				for (j=0; j<imgs.length; j++) {
					if (imgs[j].nodeName == 'IMG') {
						imgs[j].nextSibling.style.display = 'inline';
						}
					}
				}
			}
	
	}


function revealphones (node) { 
	var displayareaname = node.parentNode.parentNode.parentNode.id;
	var displayarea = document.getElementById('display'+displayareaname);
	span = node.nextSibling; 
	cloneddata = span.cloneNode(true); 
	cloneddata.style.display = 'inline';
	var characters = cloneddata.getElementsByTagName( 'img' );

	displayarea.removeChild(displayarea.firstChild);
	displayarea.appendChild(cloneddata);
	displayarea.style.display = 'block';
	//span.style.display = 'inline';
	}
	

function oldrevealphones (node) { 
	displayarea = node.parentNode.parentNode.lastChild;
	//displayarea = document.getElementById('sounddisplay');
	//displayarea = node.parentNode.nextSibling;
	span = node.nextSibling; 
	cloneddata = span.cloneNode(true); 
	cloneddata.style.display = 'inline';
	var characters = cloneddata.getElementsByTagName( 'img' );
	for (var j = 0; j < characters.length; j++ ) {
		if ((! characters[j].className.match(/ph/)) && (! characters[j].className.match(/noMouseover/))) { 
			setMouseover(characters[j]);
			setMouseout(characters[j]);
			setOnclickPhone(characters[j], characters[j].alt);
			}
		else if (characters[j].className.match(/ph/)) {
			
			}
		else {
			setBlankMouseover(characters[j]);
			}
		}

	displayarea.removeChild(displayarea.firstChild);
	displayarea.appendChild(cloneddata);
	displayarea.style.display = 'block';
	//span.style.display = 'inline';

	// figure out distance from left edge to position result
	margin = 0;
	while (node.previousSibling) {
		if (node.previousSibling.nodeType == 1 && node.previousSibling.nodeName == 'IMG') { 
			margin += node.previousSibling.width+5; 
			}
		node = node.previousSibling;
		}
	cloneddata.style.marginLeft = margin+'px';
	displayarea.focus();
	}
	
function addfromtranscript (node) {
	span = node.nextSibling;
	if (span.style.display != 'none') { span.style.display = 'none'; return; }
	if (span.childNodes.length > 2) { span.style.display = "inline"; }
	else { addandcapture(span.firstChild.nextSibling.alt, span.firstChild.nextSibling); }
	}
