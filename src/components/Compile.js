https://web.archive.org/web/20141010035745/http://gnupdf.org/Introduction_to_PDF


function buildFile() {
    var size = 2;
    var length = 500;
}

function encapsulate(data) {
    return `<<\n${data}>>\n`;
}

function getObjectIndirectReference(objectPosition, objectRevision = 0, reference = false){ 
    // eg 3 0 R
    return `${objectPosition} ${objectRevision + (reference ? ' R' : '')}`;
}

function buildObjectBase(header, trailer, data) {
    
    return `${header}\n${encapsulate(data)}${trailer}\n`;
}

function buildHeader(objectPosition, objectRevision, type){
    //eg 3 0 R obj
    return `${getObjectIndirectReference(objectPosition, objectRevision)} ${type}`;
}

function buildPages(pageWidth, pageHeight, pageCount) {
    var data;
    
    data = `/Type /Pages\n`;
    //page size
    data += `/MediaBox [ 0 0 ${pageWidth} ${pageHeight} ]\n`;
    
    //pages
    data += `/Count ${pageCount}\n`;
    
    data += `/Kids [ ${getObjectIndirectReference(3, 0, true)} ]\n`
    return buildObjectBase(buildHeader(2, 0, "obj"), "endobj", data);
}

function buildCatalog() {
    var data;
    
    data = `/Type /Catalog\n`;
    data += `/Pages ${getObjectIndirectReference(2, 0, true)}\n`;
    return buildObjectBase(buildHeader(1, 0, "obj"), "endobj", data);
}
/*
function buildObject(objectPosition, objectRevision, type) {
    var data;
    
    data = `/Type ${type}` + "\n";
    
    return buildObjectBase(objectPosition, objectRevision, "obj", "endobj", data);
}
*/

function buildTrailer(size) {
    var data;
    
    data = `/Size ${size + 1}\n`;  // + 1 for the trailer
    data += `/Root ${getObjectIndirectReference(1, 0, true)}\n`;
    return buildObjectBase("trailer", "startxref", data);
}

function buildContent(position) {
    var data;
    
    length = 44;
    
    data = `/Length ${length}\n`;
    
    return buildObjectBase(buildHeader(position, 0, "obj"), "endobj", data);
}

function buildPage(pagePosition, parentPosition, fontPosition, contentsPosition) {
    var data;
    
    data = `/Type /Page\n`;
    data += `/Parent ${getObjectIndirectReference(parentPosition, 0, true)}\n`;
    data += `/Resources ${encapsulate(`/Font ${encapsulate(`/F1 ${getObjectIndirectReference(fontPosition, 0, true)}\n`)}`)}`;
    data += `/Contents ${getObjectIndirectReference(contentsPosition, 0, true)}\n`;
    
    return buildObjectBase(buildHeader(pagePosition, 0, "obj"), "endobj", data);
}

function buildFont(fontPosition) {
    var data;
    
    data = "/Type /Font\n";
    data += "/Subtype /Type1\n";
    data += "/BaseFont /Courier\n";
    
    return buildObjectBase(buildHeader(fontPosition, 0, "obj"), "endobj", data);
}

const version = 1.7;


var pageCount = 2;
var length = 500;

var data;


//version
data = `%PDF-${version}` + "\n";

const pagesRootPosition = 2; 
const pageWidth = 8000;
const pageHeight = 5000;

data += buildCatalog() + "\n";
data += buildPages(pageWidth, pageHeight, pageCount) + "\n";

var totalObjects = 2;//for catalog and pages


for(let i = 0; i < pageCount; i++) {
    
    var pagePosition = pagesRootPosition + i + 1;//+ 1 so the page index is not 0
    var fontPosition = pagePosition + 1;
    var contentPosition = pagePosition + 2;
    
    data += buildPage(pagePosition, pagesRootPosition, fontPosition, contentPosition, "Page") + "\n";
    totalObjects++;
    
    data += buildFont(fontPosition) + "\n";
    totalObjects++;
    
    var contentCount = 2;//Contents in page
    
    for(let j = 0; j < contentCount; j++) {
        data += buildContent(contentPosition + j) + "\n";
        totalObjects++;
    }
}

data += buildTrailer(totalObjects);

data += `${length}\n`;
data += "%%EOF";

console.log(data);