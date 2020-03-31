//
//  BarChart.swift
//  MoneyManaged
//
//  Created by Rohan Garg on 2020-03-27.
//  Copyright © 2020 RoFadez. All rights reserved.
//

import UIKit
import Charts

class BarChart: UIView {
let barChartView = BarChartView()
    var dataEntry: [BarChartDataEntry] = []
    
    var months = [String]()
    var amount = [String]()
    
    var delegate: GetChartData!{
        didSet {
            populateData()
            barChartSetUp()
        }
    }
    func populateData(){
        months = delegate.duration
        amount = delegate.amount
    }
    func reloadData(){
         setBarChart(dataPoints: months, values: amount)
    }
    func barChartSetUp(){
        
        self.backgroundColor = UIColor.init(displayP3Red: 240, green: 235, blue: 214, alpha: 0)
        self.addSubview(barChartView)
        barChartView.translatesAutoresizingMaskIntoConstraints = false
        barChartView.topAnchor.constraint(equalTo: self.topAnchor, constant: 20).isActive = true
        barChartView.bottomAnchor.constraint(equalTo: self.bottomAnchor).isActive = true
        barChartView.leadingAnchor.constraint(equalTo: self.leadingAnchor).isActive = true
        barChartView.trailingAnchor.constraint(equalTo: self.trailingAnchor).isActive = true
        barChartView.animate(xAxisDuration: 2.0, yAxisDuration: 2.0, easingOption: .easeInBounce)
        //need to stop hardcoding this u fuck
        barChartView.extraBottomOffset = 20
        setBarChart(dataPoints: months, values: amount)
    
        
    }
    
    func setBarChart(dataPoints: [String], values: [String]) {
        barChartView.noDataTextColor = UIColor.systemPink
        barChartView.noDataText = "No data for the chart you fuck"
        for i in 0..<dataPoints.count {
            print("iteration "  + " for datapoint " + dataPoints[i])
            let dataPoint = BarChartDataEntry(x: Double(i), y: Double(values[i])!)
            dataEntry.append(dataPoint)
        }
        
        let chartDataSet = BarChartDataSet(entries: dataEntry, label: "BPM")
        let chartData = BarChartData()
        chartData.addDataSet(chartDataSet)
        chartData.setDrawValues(false)
        chartDataSet.colors = [UIColor.blue]
        
        let formatter: ChartFormatter = ChartFormatter()
        formatter.setValues(values: dataPoints)
        let xaxis:XAxis = XAxis()
        xaxis.valueFormatter = formatter
        barChartView.xAxis.labelPosition = .bottom
        barChartView.xAxis.drawGridLinesEnabled = false
        barChartView.xAxis.valueFormatter = xaxis.valueFormatter
        barChartView.chartDescription?.enabled = false
        barChartView.legend.textColor = UIColor.black
        barChartView.legend.enabled = true
        barChartView.rightAxis.enabled = true
        barChartView.leftAxis.drawGridLinesEnabled = false
        barChartView.leftAxis.drawLabelsEnabled = true
        barChartView.data = chartData
        barChartView.xAxis.labelTextColor = UIColor.black
//        barChartView.xAxis.axisMinimum = 2
//        barChartView.setVisibleXRangeMaximum(10)
        //barChartView.scaleYEnabled = false
        
        
    }
    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */

}
