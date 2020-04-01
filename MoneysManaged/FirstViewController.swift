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
    func getChartData(with dataPoints: [String], values: [String])
    var duration: [String] {get set}
    var amount: [String] {get set}
}

class FirstViewController: UIViewController,  GetChartData, UIScrollViewDelegate {
    func getChartData(with dataPoints: [String], values: [String]) {
        self.duration = dataPoints
        self.amount = values
    }
    
    private var request: AnyObject?
    var duration: [String] = []
    var amount: [String] = []
    var chartView: BarChart!
        
    @IBOutlet weak var scrollChartContainer: UIScrollView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        populateChartData()
        barChart()
    }

    func populateChartData(){
        duration = []
        amount = []
        fetchStoreData()
    }
    
    func configureUI(with stores: [Store]){
        for each in 0...10{
            duration.append(stores[each].name ??  "NA")
            amount.append(stores[each].spent?.description ?? "50")
        }
        self.getChartData(with: duration, values: amount)
        self.chartView.setBarChart(dataPoints: duration, values: amount)
    }
    
    func barChart(){
        let barChart = BarChart(frame: CGRect(x:0.0, y:0.0, width: (self.view.frame.width*4), height:self.scrollChartContainer.frame.height))
        barChart.delegate = self
        self.chartView = barChart
        scrollChartContainer.delegate = self
        scrollChartContainer.contentSize = CGSize.init(width: chartView.frame.width, height: chartView.frame.height)
        scrollChartContainer.addSubview(self.chartView)
    }
}

private extension FirstViewController {
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
