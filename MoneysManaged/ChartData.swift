//
//  ChartData.swift
//  MoneysManaged
//
//  Created by Rohan Garg on 2020-03-29.
//  Copyright © 2020 RoFadez. All rights reserved.
//

import Foundation

struct Store {
    let name: String?
    let spent: Float?
}

extension Store: Decodable {
    enum CodingKeys: String, CodingKey {
        case name
        case spent
    }
}




struct Wrapper<T: Decodable>: Decodable {
    let names: [T]
}
