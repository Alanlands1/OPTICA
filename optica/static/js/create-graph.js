/*
 * Parse the data and create a graph with the data.
 */
function parseData(e) {
	var array = e.split(',');
	console.log(array);
	createGraph(array);
	return array[5];
}

function createGraph(array) {

	 nodr=['No DR'];
	 mild=['Mild'];
	 moderate=['Moderate'];
	 severe=['Severe'];
	 pro=['Proliferative DR'];

	nodr.push(Number(array[0])*100);
	mild.push(Number(array[1])*100);
	moderate.push(Number(array[2])*100);
	severe.push(Number(array[3])*100);
	pro.push(Number(array[4])*100);

	var chart = c3.generate({
		bindto: '#chart',
		data: {
			columns: [
				nodr,
				mild,
				moderate,
				severe,
				pro
			],
			type: 'bar'
		},
		bar: {
			width: {
				ratio: 0.5
			}
		}
	});
}
