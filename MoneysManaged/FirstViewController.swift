//
//  FirstViewController.swift
//  MoneysManaged
//
//  Created by Rohan Garg on 2020-03-28.
//  Copyright © 2020 RoFadez. All rights reserved.
//

import UIKit
import Charts
protocol GetChartData {
    func getChartData(with dataPOints: [String], values: [String])
    var duration: [String] {get set}
    var amount: [String] {get set}
}
class FirstViewController: UIViewController,  GetChartData {
    func getChartData(with dataPOints: [String], values: [String]) {
        self.duration = dataPOints
        self.amount = values
    }
    private var request: AnyObject?
    var duration: [String] = []
    
    var amount: [String] = []
   var chartView: BarChart!
    
    @IBOutlet weak var scrollChartContainer: UIScrollView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        populateChartData()
        fetchStoreData()
        barChart()
        print("d")
    }

    func populateChartData(){
        duration = []
        amount = []
//        self.getChartData(with: duration, values: amount)
    }
    
    func barChart(){
        let heights = self.view.frame.height - (self.tabBarController?.tabBar.frame.height ?? 0.0)
        let barChart = BarChart(frame: CGRect(x:0.0, y:0.0, width: (self.view.frame.width*2), height: heights))
        barChart.delegate = self
        self.chartView = barChart
        //we need to set a way to make extra
        scrollChartContainer.addSubview(self.chartView)
    }

}

public class ChartFormatter: NSObject, IAxisValueFormatter {
    var duration = [String]()
    
    public func stringForValue(_ value: Double, axis: AxisBase?) -> String {
        return duration[Int(value)]
    }
    
    public func setValues(values: [String]){
        self.duration = values
    }
    
}

private extension FirstViewController {
    func configureUI(with stores: [Store]){
        print("configuring")
        for each in 0...10{
            duration.append(stores[each].name ??  "NA")
            amount.append(stores[each].spent?.description ?? "50")
            print(stores[each])
        }
        print(duration[0])
        self.getChartData(with: duration, values: amount)
        self.chartView.setBarChart(dataPoints: duration, values: amount)
        print(duration[0])
        
    }
    func fetchStoreData(){
        let storeRequest = ApiRequest(resource: StoresResource())
        request = storeRequest
        storeRequest.load {[weak self] (stores: [Store]?) in
            guard let stores = stores else {
                    return
            }
            self?.configureUI(with: stores)
        }
    }
}
