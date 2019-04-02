// Loads JSON OCR files and builds index.
//
// directory_name/file_name
// directory_name = s3_bucket name
//
// Build tables to allow us to search for keywords
// keyword: { description }
//
// description contains:
// geometry of word, name of document, name of collection
//
// API:
// Allows retrieving document list containing keyword and
// word_list = FindInDocument(keyword)
// document_list = GetDocumentsFromWOrdList(word_list)
//
const fs = require("fs");
const { prompt } = require('inquirer');

function getFiles(folder) {
	var outFiles = [];

	if (typeof fs == "undefined") {
    console.log("error, fs undefined");
		return outFiles;
	}

  var dir = folder;
	var files = fs.readdirSync(dir);
	for (var i = 0; i < files.length; i++) {
		var f = files[i];
		var fn = f.substring(f.lastIndexOf("/") + 1);
		try {
			// console.log("reading", dir + f);
			var stats = fs.statSync(dir + f);
			if (stats.isFile()) {
				outFiles.push(dir + f);
			}
		}
		catch (ex) {
			// Handle error(s) here
			console.log(ex);
		}
	}

	return outFiles;
}

function readTextFile(file, callback) {
  // readFileSync does a synchronous read.
	fs.readFile(file, "utf8", function (err, data) {
		if (err) throw err;
		callback(data, file);
	});
}

// console.log("creating BlockIndex");
let BlockIndex = new Object();

function TextToIndex(text, fileName) {
	if (!text) {
		console.log("skipping");
		return;
	}
	var data = JSON.parse(text);
	// console.log(data);
	for (let block of data["Blocks"]) {
		if (block["BlockType"] == "WORD") {
			if (!block["Text"])
				break;
			key = block["Text"].toLowerCase();
			if (!BlockIndex[key]) {
				BlockIndex[key] = [];
			} else {
				// console.log('key found', key);
			}
			let Entry = {
				"doc": fileName,
				"block": block,
			};
			BlockIndex[key].push(Entry);
			// console.log(key, BlockIndex[key]);
			// console.log(Object.keys(BlockIndex).length);

		}
	}
}

function BuildIndexFromFiles(myFiles) {
	console.log("Shards read:", myFiles.length);
	for (fileName of myFiles) {
		readTextFile(fileName, TextToIndex);
	}
}

function print(key) {
	console.log(key);
}

function searchKeyword(keyword) {
	if (!BlockIndex[keyword]) {
		console.log(keyword, "not found.");
    return;
  }
  // for (key of Object.keys(BlockIndex)) {
  //   print(key);
  // }
  return BlockIndex[keyword];
}

function getFilesNamesFromSearchResult(results) {
  fileNames = {};
  for (result of results) {
    fileNames[result.doc] = '';
  }
  return Object.keys(fileNames);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Removes last segment of string with deparators.
// ie:  removeLastSegment('aa.bb.cc') => 'aa.bb'
function removeLastSegment(text, separator = '.') {
	segments = text.split(separator);
	if (segments.length <= 1) {
		return text;
	}
	return segments.splice(0,segments.length - 1).join(separator);
}

async function main() {
  const dir = "/Users/tvykruta/Documents/src/textract/output_json/ocr-data-set/";
  var myFiles = getFiles(dir);
  // console.log(myFiles);
  BuildIndexFromFiles(myFiles, BlockIndex);
  while (Object.keys(BlockIndex).length < myFiles.length) {
    await sleep(100);
  }
	console.log("index built:", Object.keys(BlockIndex).length);
	console.log("DeepFraud OCR Search Engine Initialized.");
  // result = searchKeyword("Buddd");
  // print(result);
  // result = searchKeyword("Budd");
  // print(result);
  // result = searchKeyword("Nevada");
  // if (result) {
  //   filenames = getFilesNamesFromSearchResult(result);
  // }
	// print(filenames);


	const questions = [
	{
			type: 'input',
			name: 'search',
			message: 'Enter search terms:',
	}];
	while (true) {
    await prompt(questions).then((answers) => {
			let terms = answers['search'].split(' ');
			if (terms.length > 2) {
				print("Maximum of 2 terms supported.");
				return;
			}
			print('Searching: ' + answers['search']);
			let results = []
			for (index in terms) {
				response = searchKeyword(terms[index].toLowerCase());
				if (response) {
					results.push(getFilesNamesFromSearchResult(response));
				} else {
					results.push([]);
				}
			}
			let result = results[0];
			// Compute intersection of the two arrays.
			if (results.length >= 2) {
				result = results[0].filter(x => results[1].includes(x));
				// console.log(results);
				// console.log('result intersection:' + result)
			}
			if (result) {
				print('*** Found ' +  result.length +  ' results:');
				for (file of result) {
					let pieces = file.split('/');
					let display = removeLastSegment(pieces[pieces.length - 1])
					print(display);
				}
			} else {
				print('Not found.');
			}
    });
  }
}

main();
