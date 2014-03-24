import argparse
import ast
import os
import pickle

import chef_scripts


def create_chef():
    with open(args.prop_file, 'rb') as f:
        properties = dict(pickle.load(f))
    os.remove(args.prop_file)

    jump_enabled = ast.literal_eval(args.jump_enabled)
    script = chef_scripts.ChefScripts(properties[chef_scripts.USERNAME],
                                      properties[chef_scripts.HOST],
                                      properties[chef_scripts.PRIVATE_KEY],
                                      jump_enabled, args.jump_user,
                                      args.jump_key, args.jump_port,
                                      args.jump_host, args.sftp_retries,
                                      args.rubygem_path,
                                      args.berkshelf_version,
                                      args.librarian_chef_version)

    remote_path = script.create_remote_folder(args.chef_solo_path)
    kitchen_path = script.create_remote_folder(remote_path,
                                               name=args.resource_id)
    script.bootstrap(version=properties[chef_scripts.CHEF_VERSION],
                     exec_path=kitchen_path)

    knife_path = os.path.join(kitchen_path, 'knife.rb')
    if properties[chef_scripts.KITCHEN]:
        script.clone_kitchen(properties, exec_path=kitchen_path)
    else:
        script.create_remote_kitchen(properties, kitchen_path, knife_path)

    data_bag_secret = script.databags(properties, kitchen_path, knife_path)
    script.kniferb(properties, kitchen_path, knife_path, remote_path,
                   data_bag_secret=data_bag_secret)
    node_folder = script.create_remote_folder(kitchen_path, name="nodes")
    node_file_name = properties[chef_scripts.HOST] + ".json"
    node_path = script.write_remote_json(node_folder, node_file_name,
                                         properties[chef_scripts.NODE])

    script.run_chef(knife_path, node_path, exec_path=kitchen_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prop-file')
    parser.add_argument('--resource-id')
    parser.add_argument('--chef-solo-path', default="/tmp/chef")
    parser.add_argument('--sftp-retries', type=int)
    parser.add_argument('--jump-enabled')
    parser.add_argument('--jump-host')
    parser.add_argument('--jump-port')
    parser.add_argument('--jump-user')
    parser.add_argument('--jump-key')
    parser.add_argument('--rubygem-path')
    parser.add_argument('--berkshelf-version')
    parser.add_argument('--librarian-chef-version')
    args = parser.parse_args()

    try:
        create_chef()
    finally:
        if os.path.isfile(args.prop_file):
            os.remove(args.prop_file)