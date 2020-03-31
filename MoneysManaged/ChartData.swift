//
//  ChartData.swift
//  MoneysManaged
//
//  Created by Rohan Garg on 2020-03-29.
//  Copyright © 2020 RoFadez. All rights reserved.
//

import Foundation

struct ChartData{
    var url = "http://127.0.0.1:5000/"
}
 

protocol ApiResource {
    associatedtype ModelType: Decodable
    var methodPath: String { get }
}

extension ApiResource {
    var url: URL {
        var components = URLComponents()
        components.host =  "127.0.0.1"
        components.scheme = "http"
        components.port = 5000
        components.path = methodPath
        
        components.queryItems = [
            URLQueryItem(name: "query", value: "spent")
        ]
        print(components.url?.absoluteString as Any)
        return components.url!
    }
}


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

struct StoresResource: ApiResource {
    typealias ModelType = Store
    let methodPath = "/stores"
}

protocol NetworkRequest: AnyObject {
    associatedtype ModelType
    func decode(_ data: Data) -> ModelType?
    func load(withCompletion completion: @escaping(ModelType?) -> Void)
}

extension NetworkRequest {
    fileprivate func load(_ url: URL, withCompletion completion: @escaping (ModelType?) -> Void) {
        let session = URLSession(configuration: URLSessionConfiguration.default, delegate: nil, delegateQueue: .main)
        let task = session.dataTask(with: url, completionHandler: { [weak self] (data: Data?, response: URLResponse?, error: Error?) -> Void in
            guard let data = data else {
                completion(nil)
                return
            }
            completion(self?.decode(data))
        })
        task.resume()
    }
}

class ApiRequest<Resource: ApiResource> {
    let resource: Resource
    
    init(resource: Resource) {
        self.resource = resource
    }
}

extension ApiRequest: NetworkRequest {
    func decode(_ data: Data) -> [Resource.ModelType]? {
        let wrapper = try? JSONDecoder().decode(Wrapper<Resource.ModelType>.self, from: data)
        return wrapper?.names
    }
    
    func load(withCompletion completion: @escaping ([Resource.ModelType]?) -> Void) {
        load(resource.url, withCompletion: completion)
    }
}
struct Wrapper<T: Decodable>: Decodable {
    let names: [T]
}
