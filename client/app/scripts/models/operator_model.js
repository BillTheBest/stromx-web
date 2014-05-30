/* global App */

App.Operator = DS.Model.extend({
  name: DS.attr('string'),
  status: DS.attr('string'),
  type: DS.attr('string'),
  package: DS.attr('string'),
  version: DS.attr('string'),
  parameters: DS.hasMany('parameter', {async: true})
});

App.Operator.FIXTURES = [
  {
    id: 0,
    name: 'Generate numbers',
    status: 'initialized',
    type: 'Counter',
    package: 'runtime',
    version: '0.3.0',
    parameters: []
  },
  {
    id: 1,
    name: 'Send numbers',
    status: 'initialized',
    type: 'Send',
    package: 'runtime',
    version: '0.3.0',
    parameters: [1]
  },
  {
    id: 2,
    name: 'Blur the image',
    status: 'none',
    type: 'Blur',
    package: 'cv::imgproc',
    version: '0.0.1',
    parameters: [2, 3, 4, 6, 7, 12]
  },
  {
    id: 3,
    name: 'Receive remote images',
    status: 'none',
    type: 'Receive',
    package: 'runtime',
    version: '0.0.1',
    parameters: [5]
  },
  {
    id: 4,
    name: 'Test operator',
    status: 'none',
    type: 'Test',
    package: 'mypackage',
    version: '0.0.1',
    parameters: [8, 9, 10, 11]
  }
];